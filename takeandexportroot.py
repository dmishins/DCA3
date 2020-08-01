import matplotlib.pyplot as plt
import numpy as np
import argparse
import os
import datetime
import binascii
import struct
from math import floor, ceil


parser = argparse.ArgumentParser(
    description='Take and process data from DAPHNE board')
# Arguments about input file and bin format
parser.add_argument('filename', nargs='?')
parser.add_argument('--directory', action='store_true',
                    help='directory of bin files to process')
parser.add_argument('--ignore_timestamp', action='store_true',
                    help='ignore timestamp')
parser.add_argument('--PROMPT1', action='store_true',
                    help='Skip one prompt at the beginning of the spill (after wc)')
parser.add_argument('--PROMPT2', action='store_false',
                    help='DO NOT Skip one prompt at the beginning of the spill (after header)')

# Actions
parser.add_argument('-p', action='store', nargs='*', type=int,
                    help='plot channels')
parser.add_argument('--fft', action='store', nargs='*', type=int,
                    help='plot fft channels')
parser.add_argument('--hist', action='store', nargs='*', type=int,
                    help='plot max adc hist for channels')
parser.add_argument('--ahist', action='store', nargs='*', type=int,
                    help='plot area  hist for channels')
parser.add_argument('--plota0', action='store_true',
                    help='plot a0 current readings and stop')
parser.add_argument('--darkrate', action='store_true',
                    help='plot dark rate measurements')
# Modifiers

parser.add_argument('--super', action='store_true',
                    help='superimpose plots')
parser.add_argument('--pltnum', action='store', type=int,
                    help='number of signals to plt.')
parser.add_argument('--filter', action='store', nargs='*',
                    help='filter based on following channels.  Currently filter settings must be changed by editing code')
parser.add_argument('--verbose', action='store_true',
                    help='prints additional info')

parser.add_argument('--verbose2', action='store_true',
                    help='prints additional info(waveforms of plots)')
parser.add_argument('--exact_name', action='store_true',
                    help='uses exact filename')

# ROOT
parser.add_argument('--root', action='store',
                    help='output root ttree file. Requires root installation')

args = parser.parse_args()


def signed(val):
    if val > 2048:
        return val - 4096
    return val


def plota0(filename):
    file = open(filename, "r")
    lines = file.readlines()
    ch = np.array([int(line.split(":")[0]) for line in lines])
    a0 = [float(line.split(":")[1]) for line in lines]
    a0 = [8.192-val if val > 4.096 else val for val in a0]
    a0 = np.array(a0) / 8.0 * 250.0
    #print(ch, a0)
    plt.plot(ch, a0, marker='o')
    plt.show()


def plotchannel(events, ch, super=False):
    plt.figure("Waveform")
    for i, indiv_event in enumerate(events[:args.pltnum]):
        if ch in indiv_event.wave:
            plt.plot(indiv_event.wave[ch], label=("EV: " + str(i)))
            if args.verbose2:
                print(indiv_event.wave[ch])
            plt.xlabel('ticks (12.55 ns)')
            plt.ylabel('ADC')
            if super == False:
                plt.title("CH: " + str(ch) + " Trigger: " +
                          str(indiv_event.tc))
                plt.show()
            else:
                plt.title(pltttl)
                plt.show(block=False)


def plotdarkrate(events):
    counts = {}
    ticks = {}
    for i, indiv_event in enumerate(events[:args.pltnum]):
        for ch in indiv_event.pulsecount.keys():
            if not ch in counts:
                counts[ch] = 0
                ticks[ch] = 0
            #print("hi", ch, counts[ch], ticks[ch])
            counts[ch] += indiv_event.pulsecount[ch]
            ticks[ch] += len(indiv_event.wave[ch])
    countlist = sorted(counts.items())
    tickslist = sorted(ticks.items())
    counts = np.array(list((x[1] for x in countlist)))
    ticks = np.array(list((x[1] for x in tickslist)))
    charr = np.array(list((x[0] for x in tickslist)))
    rate = counts/ticks * 8 * 10**7
    plt.plot(charr, rate)


def histchannel(events, ch):
    plt.figure("MAX ADC Histogram")
    maxadcvals = []
    for i, indiv_event in enumerate(events[:args.pltnum]):
        if ch in indiv_event.wave:
            maxadcvals.append(indiv_event.maxadc[ch])
    plt.hist(maxadcvals, bins=list(
        range(min(maxadcvals)-1, max(maxadcvals) + 3, 1)), histtype='step')
    plt.xlabel('MAX ADC value in event')
    plt.ylabel('# Of events')
    plt.title("MAX ADC Histogram  CH:" + str(ch))
    plt.yscale('log')
    # plt.show()


def ahistchannel(events, ch):
    plt.figure("Area Histogram")
    areavals = []
    for i, indiv_event in enumerate(events[:args.pltnum]):
        if ch in indiv_event.wave:
            areavals.append(indiv_event.area[ch])
    # range(int(floor(min(areavals))), int(ceil(max(areavals))) + 1, 1))
    plt.hist(areavals, bins=50, histtype='step')

    plt.xlabel('Area around max adc value in event')
    plt.ylabel('ADC')
    plt.title("Area Around Max Histogram  CH: " + str(ch))
    # plt.yscale('log')
    # plt.show()


def fftchannel(events, ch, super=False):
    f_s = 1 / 12.55e-9

    plt.figure("FFT")
    totalfft = np.zeros(239, dtype=np.complex128)
    for i, indiv_event in enumerate(events[:args.pltnum]):
        if ch in indiv_event.wave:
            evchdata = indiv_event.wave[ch]
            eventfft = np.fft.fft(evchdata)
            freqs = np.fft.fftfreq(len(evchdata)) * f_s
            if np.shape(eventfft) == (239,):
                totalfft = totalfft + abs(eventfft)
            else:
                print("Bad FFT")
            # plt.xlim(0,f_s//1e6//2)
            # plt.title(ch + " FFT")
            # plt.ylim((0, 30000))

            # plt.title(ch)
            if super == False:
                plt.plot(abs(freqs/1e6), abs(eventfft))
                plt.title(str(ch) + " Event: " + str(i + 1))
                plt.show()
    plt.plot(abs(freqs / 1e6), abs(totalfft))
    plt.title("Total (Sum) FFT CH: " + str(ch))
    plt.xlabel('Frequency (MHz)')
    plt.show()


def filter(events, ch):
    filteredevents = []
    for i, indiv_event in enumerate(events):  # [events[x] for x in noisy]:
        fft = np.fft.fft(indiv_event.wave[ch])
        if max(abs(fft[8:11])) < 275:
            filteredevents.append(indiv_event)
    return filteredevents


def exportroot(events):
    try:
        from ROOT import TFile, TTree
        from array import array
    except:
        print("Unable to import ROOT")
        return
    f = TFile(args.root, 'recreate')
    t = TTree('t1', 'adc data')

    maxn = event.maxlen
    print(maxn)
    d1 = array('i', maxn * [0])
    d2 = array('i', maxn * [0])
    d3 = array('i', maxn * [0])
    d4 = array('i', maxn * [0])

    t.Branch('ch1', d1, 'ch1[' + str(maxn) + ']/I')
    t.Branch('ch2', d2, 'ch2[' + str(maxn) + ']/I')
    t.Branch('ch3', d3, 'ch3[' + str(maxn) + ']/I')
    t.Branch('ch4', d4, 'ch4[' + str(maxn) + ']/I')

    for event in events:
        for j in range(event.eventlength):
            d1[j] = event.ch1[j]
            # print d1[j]
            d2[j] = event.ch2[j]
            d3[j] = event.ch3[j]
            d4[j] = event.ch4[j]
        # print d1
        t.Fill()
    # t.Print()
    # t.Show(0)
    # t.Show(1)
    # t.Show(2)
    # t.Show(3)
    # t.Scan("*")

    f.Write()
    f.Close()


class event:
    # Each event owns a dictionary that maps channels to lists of of adc values
    headerlen = 16
    maxlen = 0
    threshold = 5

    def __init__(self, data):
        self.wave = {}
        self.maxadc = {}
        self.maxidx = {}
        self.area = {}
        self.pulsecount = {}
        self.pedistal = {}
        self.raw = data
        self.extract(data)

    def extract(self, data):
        self.headerraw = data[:event.headerlen]
        try:
            # See documentation from STEN
            self.wc, self.ts, self.tc, self.sp, self.tt, self.es = struct.unpack(
                ">HIIHHH", data[:16])
            if args.verbose:
                print(struct.unpack(">HIIHHH", data[:16]))
        except:
            print("bad event")

        if event.maxlen < self.wc:
            event.maxlen = self.wc

        ptr = event.headerlen
        while ptr < self.wc*2:
            if not (data[ptr:ptr + 1] == b"\x80"):
                print(ptr, data[ptr:ptr + 5].hex())
                print("bad channel")
                break
            chno = struct.unpack(">B", data[ptr + 1:ptr + 2])[0]
            # There appears to be an off-by-one in the FEB. here are sp-1 samples
            chraw = data[ptr + 2:ptr + 2 * self.sp]
            # print(chraw.hex())
            fmt = ">%dH" % (self.sp-1)
            self.wave[chno] = np.array([signed(x)
                                        for x in list(struct.unpack(fmt, chraw))])
            # Define the pedistal by taking the average of the first 20 ticks
            self.pedistal[chno] = int(np.average(self.wave[chno][:20]))
            self.maxadc[chno] = max(self.wave[chno])
            self.maxidx[chno] = np.where(
                self.wave[chno] == (self.maxadc[chno]))[0][0]
            self.area[chno] = np.trapz(
                self.wave[chno][self.maxidx[chno]-2:self.maxidx[chno]+2])
            self.pulsecount[chno] = np.sum(np.logical_and((np.sign(self.wave[chno] - self.pedistal[chno] - event.threshold) > 0),
                                                          (np.diff(self.wave[chno] - self.pedistal[chno] - event.threshold, prepend=0) > 0)))
            ptr += 2 * self.sp
            #print("GOODCH",chno, self.wave[chno])
        if args.verbose:
            print("Channels: ", list(self.wave.keys()))


def process_file(localpath):
    f = open(localpath, "rb")
    remote_timestamp = f.readline()
    if not args.ignore_timestamp:
        st = datetime.datetime.fromtimestamp(
            float(remote_timestamp)).strftime('%Y-%m-%d %H:%M:%S')
        print("TIMESTAMP: ", st)

    lines = f.readlines()

    dump = b"".join(lines)
    print("Buffer len: ", len(dump) // 2)

    print("Header Format")
    print("SC = Spill Count\t CM = Channel Mask\t ID = Board ID\t  S = Spill Status (Lowest 2 bits)")
    print("[WRDCNT][TRGCNT][SC][CM][ID][ S]")
    ptr = 0
    promptcount = 0

    if args.PROMPT1:
        ptr += 1
        promptcount += 1

    print(dump[:2 * 8].hex())
    print("\n")

    swc, stc, sc, cm, id, ss = struct.unpack(">IIHHHH", dump[ptr:ptr+16])
    ptr += 16
    if args.PROMPT2:
        ptr += 1
        promptcount += 1
    if dump[ptr:ptr+1] == b'\x3e':
        print("WARNING: POSSIBLE PROMPT \">\" DETECTED. USE --PROMPT2 to skip")

    trgrcv = 0
    while ptr < swc*2 + promptcount:
        #print(ptr, dump[ptr:ptr+20])
        eventwdcnt = struct.unpack(">H", dump[ptr:ptr + 2])[0]
        #wc, ts, tc, sp, tt, es = struct.unpack(">HIIHHH", data[:16])
        #print(dump[ptr:ptr + 2], eventwdcnt)
        # print("here")
        events.append(event(dump[ptr:ptr + eventwdcnt * 2]))
        ptr += eventwdcnt * 2
        trgrcv += 1
        # print("loop")
        # quit()
    print("Triggers Expected, Processed: " + str(stc) + ", " + str(trgrcv))

print("HI 123", args.p)
if args.p == [-1]:
    plotargs = list(range(63))
else:
    plotargs = args.p
if args.plota0:
    path = args.filename + ".a0"
    plota0(path)
    exit(0)
events = []
path = args.filename
if not args.exact_name:
    path = path + ".bin"
if args.directory:
    for filename in os.listdir(localpath):
        print(filename)
        process_file(path + "/" + filename)
else:
    process_file(path)

if args.filter:
    for channel in args.filter:
        events = list(filter(events, channel))

if events:
    print("Length of Event[0].ch%d: " % next(iter(events[0].wave.keys())), len(
        next(iter(events[0].wave.values()))))  # TODO
    print("Number of Events Processed: ", len(events))

    if args.root:
        print("Attempting to export events as a ROOT TFile")
        exportroot(events)
    print(args.p)
    if args.p:
        pltttl = "CH: "
        for channel in plotargs:
            pltttl = pltttl + str(channel) + " "  # plot title
            plotchannel(events, channel, super=args.super)

    if args.darkrate:
        plotdarkrate(events)

    if args.hist:
        for channel in args.hist:
            histchannel(events, channel)
            if not args.super:
                plt.show()
        plt.show()

    if args.ahist:
        for channel in args.ahist:
            ahistchannel(events, channel)
            if not args.super:
                plt.show()
        plt.show()

    if args.fft:
        pltttl = "FFT CH: "
        for channel in args.fft:
            pltttl = pltttl + str(channel) + " "
            fftchannel(events, channel, super=args.super)
    plt.show()


else:
    print("Events Empty")

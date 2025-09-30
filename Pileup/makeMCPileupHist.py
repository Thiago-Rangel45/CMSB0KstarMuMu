#!/usr/bin/env python

"""
Use this script to convert MC pileup distribution from python file to a TH1 in a ROOT file

e.g.

./makeMCPileupHist.py SimGeneral.MixingModule.mix_2017_25ns_WinterMC_PUScenarioV1_PoissonOOTPU_cfi
"""

import argparse
import importlib
import FWCore.ParameterSet.Config as cms
import os
import ROOT

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(1)
ROOT.TH1.SetDefaultSumw2()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pileup", help="Name of MC mixing pileup file")
    parser.add_argument("--Nbins", type=int, default=100)
    parser.add_argument("--min", type=int, default=0, help="minimum bin")
    parser.add_argument("--max", type=int, default=100, help="maximum bin")
    parser.add_argument("--outputFilename", default="PileupMC.root", help="Output ROOT filename")
    args = parser.parse_args()

    filename = ""
    if os.path.isfile(args.pileup):
        parts = args.pileup.split("/")
        try:
            src_ind = parts.index('src')
            parts = parts[ind:]
        except ValueError:
            "Assuming real filename, but cannot find 'src' in it"
        if 'python' in parts:
            parts.remove('python')
        filename = ".".join(parts)
        filename = os.path.splitext(filename)[0]
    else:
        filename = args.pileup

    py_file = importlib.import_module(filename)
    bins = py_file.mix.input.nbPileupEvents.probFunctionVariable
    values = py_file.mix.input.nbPileupEvents.probValue

    if min(bins) < args.min:
        raise RuntimeError("Your --min is larger than lowest bin in PU file")
    if max(bins) > args.max:
        raise RuntimeError("Your --max is lower than largest bin in PU file")

    if len(bins) != len(values):
        raise RuntimeError("#bins != # values")

    hTI = ROOT.TH1F("pileup", "pileup", args.Nbins, args.min, args.max)

    for i in range(1, args.Nbins + 1):
        try:
            # Get the lower edge of the current histogram bin
            bin_low_edge = hTI.GetBinLowEdge(i)
            # Find the index of this value in the input pileup data
            ind = bins.index(bin_low_edge)
            # Set the histogram bin content to the corresponding probability
            hTI.SetBinContent(i, values[ind])
        except ValueError as e:
            # If the value is not found in the input data, set content to 0
            print("Nothing for bin", i, "(value:", hTI.GetBinLowEdge(i), ")")
            hTI.SetBinContent(i, 0)

    f = ROOT.TFile(args.outputFilename, "RECREATE")
    # The histogram is often expected to be at the top level, not in a directory
    hTI.Write()
    f.Close()

    print("Successfully created MC pileup histogram in", args.outputFilename)
#!/usr/bin/env python

from argparse import ArgumentParser
import os
import pypiper
import sys

def _parse_cmdl(cmdl):
	parser = ArgumentParser(description="Automatic GEO SRA data downloader")
	
	parser.add_argument(
			"-b", "--bamfolder", 
			default=safe_echo("SRABAM"),
			help="Optional: Specify a location to store bam files "
			"[Default: $SRABAM:" + safe_echo("SRABAM") + "]")
	
	parser.add_argument(
			"-s", "--srafolder", default=safe_echo("SRARAW"),
			help="Optional: Specify a location to store sra files "
			"[Default: $SRARAW:" + safe_echo("SRARAW") + "]")
	
	# parser.add_argument(
	# 		"--picard", dest="picard_path", default=safe_echo("PICARD"),
	# 		help="Specify a path to the picard jar, if you want to convert "
	# 		"fastq to bam [Default: $PICARD:" + safe_echo("PICARD") + "]")
	
	parser.add_argument(
			"-r", "--srr", required=True, nargs="+",
			help="SRR files")

	parser = pypiper.add_pypiper_args(parser, groups=["pypiper", "config"])
	return parser.parse_args(cmdl)

def safe_echo(var):
	""" Returns an environment variable if it exists, or an empty string if not"""
	return os.getenv(var, "")


#def main(cmdl):

if __name__ == "__main__":
	#main(sys.argv[1:])
	cmdl = sys.argv[1:]
	args = _parse_cmdl(cmdl)

	key=args.srr[0]
	pm = pypiper.PipelineManager(	name="sra_convert",
									outfolder=args.srafolder,
									args=args)

	nfiles = len(args.srr)
	for i in range(nfiles):
		print("Processing " + str(i+1) + " of " + str(nfiles))
		infile = args.srr[i]
		srr_acc = os.path.splitext(os.path.basename(args.srr[i]))[0]
		outfile = os.path.join(args.bamfolder, srr_acc + ".bam")
		if (not os.path.isfile(infile)):
			infile = os.path.join(args.srafolder, args.srr[i] + ".sra")
			outfile = os.path.join(args.bamfolder, args.srr[i] + ".bam")
		if (not os.path.isfile(infile)):
			next

			
		cmd = "sam-dump -u {data_source} | samtools view -bS - > {outfile}".format(
			data_source=infile, outfile=outfile)
		pm.run(cmd, target=outfile)


	pm.stop_pipeline()

# phased-methylation

This package defines a pipeline for phased methylation calling on raw Nanopore
data. It has three steps:

1. Mapping reads to a reference genome ([minimap2](https://github.com/lh3/minimap2))
2. Phasing variants and reads ([longshot](https://github.com/pjedge/longshot))
3. Calling methylated bases ([megalodon](https://nanoporetech.github.io/megalodon/index.html))

## TODO

- improve documentation
- integrate [deepsignal-plant](https://github.com/PengNi/deepsignal-plant)

## Environment setup and installation
```sh
conda create -n phased-methylation -c conda-forge -c bioconda git cython pytest \
  pandas pysam pybedtools minimap2 longshot megalodon==2.3.4 gputil psutil \
  tabulate
conda activate phased-methylation
pip install ont_pyguppy_client_lib nvsmi tempfifo pyfaidx
git clone https://gitlab.com/salk-tm/phased-methylation.git
cd phased-methylation
pip install .
```

## Test run

To execute a test run of the pipeline, use the `test` subcommand

```sh
phased-methylation test <test_dir/>
```

## Usage
```
usage: phased-methylation [-h]
                          {launch,map,phase,call,test,mean,promoter,gene-body,plot,plot-genes,plot-repeats,export-metilene,export-bedgraph}
                          ...

pipeline for methylation calling

positional arguments:
  {launch,map,phase,call,test,mean,promoter,gene-body,plot,plot-genes,plot-repeats,export-metilene,export-bedgraph}
    launch              launch full pipeline
    map                 perform mapping step
    phase               perform phasing step
    call                perform methylation calling step
    test                execute test run
    mean                calculate average methylation across chromosomes
    promoter            quantify promoter methylation
    gene-body           quantify gene body methylation
    plot                plot methylation across chromosomes
    plot-genes          plot methylation profiles over genomic features
    plot-repeats        plot methylation profiles over genomic features
    export-metilene     export methylation data formatted for input into
                        metilene
    export-bedgraph     export methylation data in bedgraph format

optional arguments:
  -h, --help            show this help message and exit

```

### Input files

### Output files
Results will be written to the indicated output directory.

### Example
Minimal example:
```sh
phased-methylation launch reference.fa fast5s_dir/ output_dir/ query.fastq
```

### GPU resource management
`phased-methylation` (specifically, the `call` step using `megalodon`) requires at least one available GPU to run successfully. When the pipeline is launched, it will check for availability of the devices indicated by the `--devices` argument, defaulting to device `0`. If one or more indicated devices are not available, the user will be prompted to free up resources by terminating processes running on them:

```
Cannot launch because the following processes are occupying resources on device(s) 0:

=====  =====  ========================================  ==================
  GPU    PID  Process Name                              GPU Memory Usage
=====  =====  ========================================  ==================
    0  16397  /opt/ont/guppy/bin/guppy_basecall_server  9.80 GB
=====  =====  ========================================  ==================

Terminate these processes and continue? [y/N]:
```

Enter `y` to terminate the indicated processes and continue with the pipeline,
or enter any other input to terminate `phased-methylation`.

## Misc

Documentation from original shell script:

> IMPORTANT, this can only be run when there are no sequencing runs in progress. If
> there are they must be paused and then the guppy_basecaller needs to be killed to
> clear the GPU memory. In a terminal, type nvidia-smi and find the job ID of the
> guppy_basecaller(there may be two running).  KILL THEM all Run nvidia-smi again and
> you should see that the GPU memory usage is very low now. Start this script.  Once
> it gets to the megalodon part you can start sequencing on the PromethION again. If
> you start the sequener too soon this script will crash once it gets to the megalodon
> step

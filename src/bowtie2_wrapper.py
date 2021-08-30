"""
Wrapper script for bowtie2-align and bowtie2-build with version control
"""
import subprocess

def build(version, fasta):
    """
    Construct bowtie2 indices (.bt2 files)
    :param version: Enforces bowtie2 version number (e.g., '2.2.1')
    :param fasta: Path to FASTA containing reference sequences
    :return:
    """
    try:
        subprocess.check_output(['bowtie2-build', '-h'])
    except OSError:
        raise RuntimeError('bowtie2-build not found; check if it is installed and in $PATH\n')

    stdout = subprocess.check_output(['bowtie2-build', '--version'])
    local_version = stdout.split('\n')[0].split()[-1]
    assert version == local_version, 'bowtie2-build version incompatibility %s != %s' % (version, local_version)
    subprocess.check_call(['bowtie2-build', '-q', '-f', fasta, fasta])


def align_paired(version, refpath, fastq1, fastq2, nthreads, flags=('--quiet', '--no-unal', '--local')):
    """
    Call bowtie2-align on paired read data
    :param version: Enforces bowtie2 version number
    :param refpath: Path to bowtie2 index files (.bt2)
    :param fastq1: Files with #1 mates
    :param fastq2: Files with #2 mates
    :param flags: A tuple of bowtie2 flags such as --local
    :return:
    """

    # check that we have access to bowtie2
    try:
        subprocess.check_output(['bowtie2', '-h'])
    except OSError:
        raise RuntimeError('bowtie2 not found; check if it is installed and in $PATH\n')

    # check that version is the expected version
    stdout = subprocess.check_output(['bowtie2', '--version'])
    local_version = stdout.split('\n')[0].split()[-1]
    assert version == local_version, 'bowtie2 version incompatibility %s != %s' % (version, local_version)

    # stream output from bowtie2
    bowtie_args = ['bowtie2', '-x', refpath, '-1', fastq1, '-2', fastq2, '-p', str(nthreads)] + list(flags)
    p2 = subprocess.Popen(bowtie_args, stdout=subprocess.PIPE)
    for line in p2.stdout:
        yield line

    # exception handling


def main():
    iter = align_paired('2.1.3', 'gb-ref.fa', 'test1.fastq', 'test2.fastq')
    for line in iter:
        print(line)

if __name__ == '__main__':
    main()
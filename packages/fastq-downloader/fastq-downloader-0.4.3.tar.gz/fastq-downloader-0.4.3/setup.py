# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastq_downloader',
 'fastq_downloader.helper',
 'fastq_downloader.snakemake',
 'fastq_downloader.tests']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4', 'click', 'httpx', 'lxml']

entry_points = \
{'console_scripts': ['fastq-downloader = fastq_downloader.__main__:main']}

setup_kwargs = {
    'name': 'fastq-downloader',
    'version': '0.4.3',
    'description': '',
    'long_description': '# Fastq Downloader (WIP)\n\nThis python package let you download fastq files from ena.\nIt can automatic merge and rename fastq files based on the input file provided.\nIf you have trouble downloading this repo\'s release, please go to [fastgit](https://fastgit.xyz) to see if this project can help you.\n\n## Notice for Readme\nIf you are reading this from pypi, please go to [github](https://github.com/TTTPOB/fastq-downloader) to read the latest readme file, for I won\'t modify pypi readme unless new version released.\n\n## How to Use\n\n### Installation\n```bash\nconda create --name fastq-downloader -c conda-forge -c hcc -c bioconda aspera-cli snakemake-minimal httpx lxml click beautifulsoup4 python=3.9\n## use what ever you want to download the gist mentioned above to thisname.smk\nconda activate fastq-downloader\npip install fastq-downloader==0.4.2\n```\n\n### Usage\nmake sure to create an `info.tsv` before, you can just copy from the [GEO](https://www.ncbi.nlm.nih.gov/gds) website,\nthen go to vim, type `:set` paste to get into paste mode,\npaste the table into vim,\nand you can modify the names of samples to suit your need,\nthe downloaded file will then be renamed too.\nSave the file as whatever name you want, then exit vim\nthe white space will be auto convert to underscore\n\nfirst, we have to turn info tsv to individual sample accession files\n```bash\n## step 1\n## you can use fastq-downloader breakdown-tsv --help to view the help\nfastq-downloader breakdown-tsv \\\n  -i path/to/info.tsv \\\n  -o path/to/output/dir\n```\nAll paths can be relative paths.  \nThen we can start to download.\n```bash\n## step 2\nfastq-downloader smk \\\n  -i path/to/info.tsv \\\n  -o path/to/output/dir \\\n  -t {number_of_threads_you_want} \\\n  --download-backend ascp\n```\n\nafter the download is done, you can use `find` command to get all of the `fastq.gz` files and link them to anoter place. For example I have a bunch of file downloaded to `download` folder, the folder structure should look like this:\n```\n# this is what inside download folder\n. \n└── merged_fastq\n \xa0\xa0 ├── GSM5159835\n \xa0\xa0 │\xa0\xa0 ├── wt_1_R1.fastq.gz\n \xa0\xa0 │\xa0\xa0 └── wt_1_R2.fastq.gz\n \xa0\xa0 ├── GSM5159836\n \xa0\xa0 │\xa0\xa0 ├── wt_2_R1.fastq.gz\n \xa0\xa0 │\xa0\xa0 └── wt_2_R2.fastq.gz\n \xa0\xa0 └── GSM5159837\n \xa0\xa0     ├── wt_3_R1.fastq.gz\n \xa0\xa0     └── wt_3_R2.fastq.gz\n```\nThen execute `find -name "*fastq.gz" | xargs -I {} ln -s {} .`  \nAll `fastq.gz` files will be linked to the root of `download` folder:\n```\n.\n├── merged_fastq\n│\xa0\xa0 ├── GSM5159835\n│\xa0\xa0 │\xa0\xa0 ├── wt_1_R1.fastq.gz\n│\xa0\xa0 │\xa0\xa0 └── wt_1_R2.fastq.gz\n│\xa0\xa0 ├── GSM5159836\n│\xa0\xa0 │\xa0\xa0 ├── wt_2_R1.fastq.gz\n│\xa0\xa0 │\xa0\xa0 └── wt_2_R2.fastq.gz\n│\xa0\xa0 └── GSM5159837\n│\xa0\xa0     ├── wt_3_R1.fastq.gz\n│\xa0\xa0     └── wt_3_R2.fastq.gz\n├── wt_1_R1.fastq.gz -> merged_fastq/GSM5159835/wt_1_R1.fastq.gz\n├── wt_1_R2.fastq.gz -> merged_fastq/GSM5159835/wt_1_R2.fastq.gz\n├── wt_2_R1.fastq.gz -> merged_fastq/GSM5159836/wt_2_R1.fastq.gz\n├── wt_2_R2.fastq.gz -> merged_fastq/GSM5159836/wt_2_R2.fastq.gz\n├── wt_3_R1.fastq.gz -> merged_fastq/GSM5159837/wt_3_R1.fastq.gz\n└── wt_3_R2.fastq.gz -> merged_fastq/GSM5159837/wt_3_R2.fastq.gz\n```\nThis should add some convinience for your subsequent process.\n\n\nThese command lines should suit your need in most situations,\nfor those who want more flexiblity and control to the underlying `snakemake` workflow,\nyou can append your argument to the `-s` option of the `smk` subcommand;\nor you can directly use the snakemake file in this repo.\n\nFor other advanced use you can always use `--help`, or read the source code.\n\nIt will automatically try to download the file, check md5, retry if file integrity check failed, and merge the files if the number of files is more than 2, finally rename the files to the description you provided.\n\nprepare the info.tsv like this:\nnote the file must be tab delimited (tsv file), you can simply achieve this by paste it from the Excel or GEO website. Or from SRA Run Selector downloaded csv file.\n```\nGSM12345  h3k9me3_rep1\nGSM12345  h3k9me3_rep2\n```\n\n## Notice for Commonly Encountered Problems\n1. error from `ascp` saying `failed to authenticate`:\n  - It can be a network issue according to [this issue on github](https://github.com/wwood/kingfisher-download/issues/9) or a server issue of EBI [this post on biostar](https://www.biostars.org/p/9493414/) \n  - If you have encountered this problem, please try to delete the download target folder and change the `--download-backend` argument to `wget` to use ftp links.\n\n## Todo\n- [x] test for paired-end reads run merge\n- [ ] publish to bioconda\n- [x] if fail, retry\n- [x] use dag to run the pipeline (sort of, implemented by using snakemake)\n- [x] option to resume download when md5 not match\n- [x] option to continue from last time download\n- [x] implement second level parallelization\n\n## Known Issues\n- Will fail to download the files contains both paired-end reads and single-end reads. (yes it exists).\n\n## Update Content\n- 0.4.3:\n  - Update readme.\n  - Breakdown the download process to two steps and add new download backend and `wget`.\n- 0.3.2:\n   - Add filter for library layout (some sra entry has content mismatches its library layout)',
    'author': 'tpob',
    'author_email': 'tpob@tpob.xyz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

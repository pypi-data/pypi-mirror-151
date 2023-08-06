# cloud-downloader
====================================================================================
This is a simple python library that helps you download files from GDrive, HiDrive, Dropbox and Sharepoint/Onedrive.

## Installation

### cloud-downloader requires:

- Python (>= 3.6)
- click (>= 7.1.2)

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install cloud-downloader.

```bash
pip install cloud-downloader-equitania
```

---

## Usage

```bash
$ cloud-download --help
usage: cloud-download [--help] [--link] [--filename]
```
```bash
Options:
  --link TEXT             Shared link from cloud hoster (Supported: GDrive, nextcloud, HiDrive, Dropbox and Sharepoint/Onedrive)
  --filename TEXT         Name of file to be saved
  --help                  Show this message and exit.
```
---

## Example
```bash
# Execution with Google drive
cloud-download --link https://drive.google.com/file/d/1OrM4vfhgsj_nktRE4Awzj_ANiWgPYm/view?usp=sharing --filename test.pdf

# Execution with Dropbox
cloud-download --link https://www.dropbox.com/s/vom8egdsgsujda/qr-code.png?dl=0 --filename test.png

# Execution with hidrive
cloud-download --link https://my.hidrive.com/lnk/O85gdsBcy --filename test.zip

# Execution with Google drive
cloud-download --link https://cmcequitania-my.sharepoint.com/:b:/g/personal/l_olo_olo_vanderlei_de/ETFRJfONT19Pr-C15olJHTwehodsPypePr0ScOWILuw?e=ISj7K7 --filename test.pdf

# Execution without link and filename
cloud-download
```

This project is licensed under the terms of the **AGPLv3** license.

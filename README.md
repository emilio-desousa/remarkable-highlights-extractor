remarkable-highlights-extractor is a tool to easily extract the highlights to your favorite Personal Knowledge Manager from your remarkable documents with a UI made with ❤️ with Streamlit

# Demo

![assets/demo.gif](assets/demo.gif)

# Usage

## Install

```bash
git clone git@github.com:emilio-desousa/remarkable-highlights-extractor.git
```

```bash
cd remarkable-highlights-extractor
```

```bash
poetry install
```

## Download your remarkable documents

Add it to `data/xochitl` folder with:

- ssh and scp
- RMPAPI
- ...

## Run the streamlit app

```bash
poetry run streamlit run highlights_extractor/app/main_page.py
```

## Features

### Supported Sources

- [x] Local Files in `data/xochitl` folder
- [ ] Google Drive
- [ ] SCP
- [ ] Remarkable Cloud

### Extractors

- [x] Obsidian
- [ ] Roam Research
- [ ] Notion

## Notes

This is a free-time project, to make my life easier with my remarkable workflow and to practice some good designs in python.
For example, I have created the Extractor Abstraction to make the development of new extractor easier, so if you want to contribute it will be easier for you!

**If you have any challenge on the design, do not hesitate to open an issue, It will be a super opportunity to learn !**

# How to contribute

There is some opened issues, feel free to pick one and open a PR! There is some tagged with "good first issue" if you want to start with something easy.

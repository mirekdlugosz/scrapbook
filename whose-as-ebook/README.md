This repository contains scripts to download and transform [WHOSE website](http://whose.associationforsoftwaretesting.org/index.php?title=Main_Page) into set of markdown documents.

# Prerequisites

* [httrack](https://www.httrack.com/)
* Python 3.4 or later
* Python `lxml` package installed (use system package manager or create Python virtual environment and `pip install`)
* [pandoc](https://pandoc.org/)

# Running

```
./whose-as-markdown.sh
```

It should do everything for you:

* mirror WHOSE website locally into `./whose/web/` using httrack
* remove recurring fragments from HTML files (side menu, link to search etc.)
* convert HTML files into markdown using pandoc

# Creating ebook with WHOSE content

You can use pandoc to create ebook with WHOSE content in single file.

Main problem you will face will probably be that pandoc processes files in FIFO queue, while files on disk are sorted alphabetically by title. I imagine there is some clever trick to sort them by (source) HTML creation time, or for httrack to enumerate files as it encounters links. For now, I just specified order myself:

```
pandoc -o whose.epub --metadata title="WHOSE" \
    markdown/Main_Page.md \
    markdown/Test_Design.md \
    markdown/Identifying_and_Using_Oracles.md \
    markdown/Quick_Attacks.md \
    markdown/Black_Box_Techniques.md \
    markdown/White_Box_Techniques.md \
    markdown/Risk_Prioritization.md \
    markdown/Identifying_Combinatorial_Explosion.md \
    markdown/Establishing_Test_Objectives.md \
    markdown/Communication.md \
    markdown/Asking_Questions.md \
    markdown/Chartering.md \
    markdown/Communicating_Risk.md \
    markdown/Engaging_the_Audience.md \
    markdown/Managing_Expectations.md \
    markdown/Note_Taking.md \
    markdown/Rhetoric.md \
    markdown/Speaking_About_Testing_To_NonTesters.md \
    markdown/Community.md \
    markdown/Coaching.md \
    markdown/Community_Building.md \
    markdown/Time_Management.md \
    markdown/Knowing_When_to_Stop.md \
    markdown/Critical_Thinking.md \
    markdown/Modeling.md \
    markdown/Aristotelian_and_Predicate_Logic.md \
    markdown/Identifying_Logical_Fallicies.md \
    markdown/CriticalThinking.md \
    markdown/Management.md \
    markdown/Developing_a_Test_Strategy.md \
    markdown/WHOSE_About.md \
    markdown/WHOSE_General_disclaimer.md \
    markdown/WHOSE_Privacy_policy.md    
```

Billwarrior
============
An extension for the venerable CLI timetracker,
[Timewarrior](https://timewarrior.net/). Use Billwarrior to generate invoices in LaTeX
from your Timewarrior reports.

Trey Hunner's basic [Invoice](https://www.latextemplates.com/template/invoice) LaTeX template
(CC BY-NC-SA 3.0) is included in the `etc/latex/` directory.

Installation
-------------
By cloning the repository:

```shell
git clone http://github.com/sw00/billwarrior.git
cd billwarrior
python setup.py install
```

`setup.py` will create a directory `$HOME/.config/billwarrior/` and copy `billwarrior.ini`
as well as LaTeX files there.


Usage
------

Edit `$HOME/.config/billwarrior/billwarrior.ini` to add the categories of invoice items you'd
like to generate invoices for. For example:

```ini
[categories]
dev.tags = coding, dev, pairing
dev.text = Software Development Services
dev.rate = 44.85

consulting.tags = meeting, workshop, ceremony
consulting.text = Consulting Services
consulting.rate = 85.50

nonbillable.tags = pingpong, travel, lunch
nonbillable.text = Nonbillable Time
nonbillable.rate = 0.0

invisible.tags = invisible
invisible.rate = -1
```

1. Copy the `bin/billwarrior` script into your Timewarrior extensions directory and ensure
   that it's
   it executable

2. Run a report and pipe output to the `billwarrior_items.tex` file that's imported by
   `invoice.tex`

3. Run `pdflatex`(or `xelatex`, whatever your preference) against `invoice.tex`

```shell
cp bin/billwarrior $TIMEWARRIORDB/extensions/billwarrior
chmod +x $TIMEWARRIORDB/extensions/billwarrior
timew report billwarrior > ~/.config/billwarrior/latex/billwarrior_items.tex
cd ~/.config/billwarrior/latex && pdflatex invoice.tex
```

Additional Notes
----------------
* It's up to you to customise the LaTeX template (`invoice.tex` and `invoice.cls`).

* Billwarrior is strict. It won't run if it encounters a time interval with tags that
  isn't configured to map to a category in `billwarrior.ini`. So make sure you give
  `timew` the appropriate filters.

TODO/Issues
-----

- [ ] Automated build (GH Actions).

- [ ] Make line items' LaTeX output configurable.

- [ ] Smarter `setup.py install` to detect Timewarrior extensions path and install itself.

- [ ] Upload/distribute to the cheese shop and support installation via `pip install`

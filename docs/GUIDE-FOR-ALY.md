# Your Carry-On Checker — The Owner's Guide

Hi Aly! This is the manual for your carry-on checker website. It's written
for a human, not a programmer — you don't need any technical background to
own and run this thing. Ten minutes with this guide and you'll know how it
all works.

**The site:** https://jonfishr.github.io/carry-on-checker/ *(this address
will change if/when the project moves to your own account or domain)*

---

## What this is

A free website version of your **Carry-On Compliance Checker** spreadsheet.
Visitors type in their bag's height, width, and depth (or tap one of your
recommended bags), and instantly see how it stacks up against every
airline in your list — with your signature real-world judgment built in:

- **✅ Fits** — within the airline's published limit.
- **⚠️ Close call** — over by no more than 1 inch (2.54 cm). Your rule: bags
  this close usually slide into the sizer just fine (like your Monos on
  Air Canada).
- **❌ Too big** — more than an inch over. Trouble at the gate.

It also explains your height → width → depth hierarchy, shows your bag
notes, and groups your recommended bags into your hard-shell / soft-side /
value picks.

---

## How it works, in plain English

There are only four moving parts, and you only ever touch one of them:

1. **A Google Sheet — your control panel.** It looks almost exactly like
   your original spreadsheet: one tab for airlines, one for bags. This is
   the *only* thing you edit.

2. **GitHub — the filing cabinet.** A free service that stores the
   website's files (the page itself and two small data files). Think of it
   as a Dropbox folder with a very good memory — it remembers every version
   of every file, forever, so nothing can ever be lost by accident.

3. **GitHub Pages — the display window.** Another free service (same
   company) that takes the files in the cabinet and shows them to the world
   as a website. No servers to rent, nothing to renew, no hosting bill.
   Ever.

4. **A little robot (a "GitHub Action").** Once a day, it opens your Google
   Sheet, copies the numbers into the filing cabinet, and the display
   window updates automatically. If it finds a mistake in the sheet (say, a
   height typed into the wrong column), it *doesn't* touch the site —
   it leaves the site as-is and writes you a note describing exactly
   what's wrong.

So the whole flow is: **you edit the Sheet → the robot copies it over →
the site updates.** Usually within a day, or within about two minutes if
you press the robot's "go" button (below).

**What it costs to run: $0.** Genuinely nothing, forever, at any realistic
amount of traffic. The only thing that would ever cost money is an optional
custom web address (like `carryon.likewhereyouregoing.com`) — roughly the
price of one coffee per year, and only if you want it.

---

## Using the site (what your visitors see)

1. **Check My Bag** — type height, width, depth (including wheels and
   handles!), in cm or inches. Results appear instantly, sorted into
   ✅ / ⚠️ / ❌ groups, with a note on *which* dimension is over and by how
   much. Each airline links to its official baggage page and shows when the
   number was last checked.
2. **Bag Library** — popular carry-ons grouped by type, with your tested
   bags starred ⭐ as *Aly's picks* and shown first. "Check This Bag" pops
   a bag's measurements into the checker.
3. **How It Works** — explains the close-call rule and the measurement
   hierarchy in your voice, plus your "plan with confidence — not add
   stress" disclaimer.

---

## Updating the data (the part you'll actually do)

### Change an airline's numbers, or add a new airline

1. Open the Google Sheet (bookmark it!).
2. On the **Airlines** tab, find the airline's row and fix the numbers —
   or add a new row at the bottom and fill in: name, region, height, width,
   depth (all in **centimeters**).
3. If you can, paste the airline's official baggage page link into
   **Official source** and today's date into **Last verified** (like
   `2026-07-02`). Optional but nice — it's what makes the site trustworthy.
4. That's it. No save button needed (Google Sheets saves by itself). The
   site updates on the robot's next daily run.

### Add or change a bag

Same idea on the **Luggage** tab: bag name, category (`Hard-shell`,
`Soft-side`, `Value`, or `Luxury`), the three measurements in cm, and your
note in your own words — your notes show up on the site exactly as written.
The optional **Product link** column makes the bag's name on the site link
to that page (a store page, or your own review/affiliate link — leave it
blank and the name is just text).

The **Aly's pick** column is your star button: type `Yes` (or just `⭐`)
next to a bag and it gets a "⭐ Aly's pick" badge on the site and moves to
the front of its section. Leave it blank for regular list entries.

### Remove something

Delete the whole row in the sheet (right-click the row number → *Delete
row*). Gone from the site after the next sync.

### Want the change live *right now*?

1. Go to the project on GitHub and click the **Actions** tab.
2. Click **Update data from Google Sheet** in the left list.
3. Click the **Run workflow** button (right side), then the green
   **Run workflow** confirm button.
4. Wait ~2 minutes. Refresh your site. Done.

### Golden rules for the sheet

- **Centimeters only** — the site converts to inches for visitors
  automatically.
- **Don't rename or delete the column headers** (the gray top row). The
  robot finds everything by those names.
- **Height is the longest side** of the bag.
- Everything else — colors, bolding, sorting rows, adding your own notes
  column off to the right — is totally fine. The robot only reads the
  columns it knows.

---

## When something goes wrong

Honestly, not much can. The two failure modes:

**1. The robot finds a mistake in the sheet.** You'll see an "issue" (a
note) appear on the GitHub project titled *"Sheet sync: the Google Sheet
has a problem that needs a human."* It lists exactly which row and what's
wrong, in plain English — for example:

> `Ryanair: height 5.5 cm looks wrong (expected 40-70 cm — was it typed in
> the right column and in centimeters?)`

**The site is never harmed by this** — it just keeps yesterday's data
until you fix the row. Fix it in the sheet, run the robot manually (see
above), and the note can be closed.

The three most common mistakes, all easy fixes:
- a number typed in the wrong column (height in the depth column),
- inches typed where centimeters belong,
- a required cell left blank (name, height, width, or depth).

**2. An airline changed its rules and the sheet is out of date.** Once a
month, a second robot glances at every airline's official baggage page and
compares it with what the page looked like last month. If a page changed,
it writes you a note listing which airlines are worth a quick re-check.
(It never changes numbers itself — sizing pages are too nuanced for a
robot to be trusted with. You're the expert; it's just your lookout.)

**If you're ever stuck:** ask Jon 🙂 Nothing you can do in the sheet can
break the site.

---

## Glossary (the five words you might bump into)

| Word | What it actually means |
|---|---|
| **Repository ("repo")** | The project's folder in the GitHub filing cabinet. |
| **Commit** | One saved change to the folder, with a note about what changed. GitHub keeps them all forever. |
| **GitHub Pages** | The free service showing your folder to the world as a website. |
| **Action / workflow** | A robot with one job (e.g. "copy the sheet over every morning"). |
| **Issue** | A sticky note on the project — how the robots leave you messages. |

---

## What's under the hood (only if you're curious)

The site is one HTML file plus two small data files — no database, no
company's server, nothing that can "go down" on its own. The data files are
generated from your Google Sheet. Every change is version-controlled, so
any mistake can be undone with one click. The code is open source under
the MIT license, credited to you, with your site and channel linked
throughout.

Happy travels! ✈️

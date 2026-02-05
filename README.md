# 🧳 Carry-On Compliance Checker

**Check if your carry-on luggage fits airline size requirements**

A simple, fast tool to compare your bag against 74 airlines' carry-on policies. Created by [Aly Smalls](https://likewhereyouregoing.com).

👉 **[View Live Demo](#)** (add your GitHub Pages URL here after deployment)

---

## ✨ Features

- ✅ Check any bag dimensions against 74 airlines instantly
- ✅ Toggle between centimeters and inches
- ✅ Browse 17+ recommended, tested carry-on bags
- ✅ Mobile-friendly, responsive design
- ✅ No backend required - runs entirely in the browser
- ✅ Zero cost to host and maintain

---

## 🚀 Quick Deploy to GitHub Pages

### Option 1: Upload Files Directly (Easiest)

1. **Create a new GitHub repository**
   - Go to [github.com/new](https://github.com/new)
   - Name it `carry-on-checker` (or whatever you prefer)
   - Make it **Public**
   - Don't initialize with README

2. **Upload the files**
   - Click "uploading an existing file"
   - Drag and drop these files:
     - `index.html` (main website file)
     - `airlines.json` (airline data)
     - `luggage.json` (luggage library data)
     - `README.md` (this file)
   - Click "Commit changes"

3. **Enable GitHub Pages**
   - Go to repository **Settings**
   - Click **Pages** in the left sidebar
   - Under **Source**, select `main` branch
   - Click **Save**

4. **Access your site!**
   - Your site will be live at: `https://YOUR-USERNAME.github.io/carry-on-checker/`
   - Wait 1-2 minutes for the initial build

### Option 2: Using Git (For Developers)

```bash
# Clone this repository
git clone https://github.com/YOUR-USERNAME/carry-on-checker.git
cd carry-on-checker

# Make your changes (if any)

# Commit and push
git add .
git commit -m "Initial commit"
git push origin main
```

Then follow step 3 above to enable GitHub Pages.

---

## 🔄 How to Update Data

### When Airlines Change Their Carry-On Rules

Airlines occasionally update their carry-on size restrictions. Here's how to update them:

#### Method 1: Edit the JSON File Directly (Recommended)

1. **Edit `airlines.json` on GitHub:**
   - Navigate to the file in your repository
   - Click the pencil icon (✏️) to edit
   - Find the airline you need to update
   - Modify the dimensions:

   ```json
   {
     "id": "united",
     "name": "United Airlines",
     "dimensions": {
       "height": 56.0,    ← Change these numbers
       "width": 35.0,     ← 
       "depth": 22.0,     ← 
       "unit": "cm"
     }
   }
   ```

2. **Commit your changes:**
   - Scroll down and click "Commit changes"
   - Your site will automatically rebuild in ~30 seconds!

#### Method 2: Re-embed the Data in index.html

If you prefer to keep everything in a single file:

1. **Edit the data in `index.html`:**
   - Open `index.html` in a text editor
   - Find the line: `const AIRLINES_DATA = {`
   - Update the airline dimensions directly in the JavaScript object
   - Save the file

2. **Upload the updated file:**
   - Go to your repository on GitHub
   - Click on `index.html`
   - Click the pencil icon to edit
   - Paste your updated HTML
   - Commit changes

### When Adding New Luggage to the Library

To add new tested bags:

1. **Edit `luggage.json`:**

   ```json
   {
     "id": "new-bag-model",
     "name": "Brand Name Carry-On",
     "dimensions": {
       "height": 55.0,
       "width": 40.0,
       "depth": 20.0,
       "unit": "cm"
     },
     "notes": "Your review or notes about the bag"
   }
   ```

2. **Commit the changes** - the site updates automatically!

### Removing an Airline or Bag

Simply delete the entire object (including the curly braces `{ }`) from the JSON file, making sure to remove any trailing comma if it's the last item in the list.

---

## 📊 Data Structure Reference

### Airlines Data Format

```json
{
  "airlines": [
    {
      "id": "unique-id",           // Lowercase, no spaces
      "name": "Display Name",      // How it appears to users
      "dimensions": {
        "height": 56.0,            // Always in cm
        "width": 45.0,
        "depth": 25.0,
        "unit": "cm"               // Always "cm"
      }
    }
  ]
}
```

### Luggage Data Format

```json
{
  "luggage": [
    {
      "id": "unique-id",
      "name": "Brand Model Name",
      "dimensions": {
        "height": 55.0,
        "width": 40.0,
        "depth": 20.0,
        "unit": "cm"
      },
      "notes": "Optional description or review"
    }
  ]
}
```

**Important Notes:**
- All dimensions must be in **centimeters** (the site handles conversion to inches automatically)
- The `id` field should be lowercase with hyphens instead of spaces
- Dimensions use decimal points (e.g., `55.0` not `55`)

---

## 🛠️ Technical Details

### File Structure

```
carry-on-checker/
├── index.html          # Main website (includes embedded data)
├── airlines.json       # Airline carry-on size data
├── luggage.json        # Recommended luggage library
└── README.md          # This file
```

### How It Works

- **100% static**: No server, database, or API required
- **Client-side only**: All calculations happen in the browser
- **Data embedded**: JSON data is embedded directly in the HTML for instant loading
- **Responsive**: Works on desktop, tablet, and mobile devices

### Browser Compatibility

Works in all modern browsers:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

---

## 🎨 Customization

### Changing Colors

Edit the CSS variables in `index.html` (around line 15):

```css
:root {
    --primary-teal: #5a9a9f;      /* Main brand color */
    --dark-teal: #3d7175;         /* Hover states */
    --soft-sage: #a8b5a0;         /* Accent color */
    --cream: #f7f5f0;             /* Background */
    /* ... more colors ... */
}
```

### Changing Fonts

The site uses Google Fonts (Lora + Montserrat). To change:

1. Find the Google Fonts link in the `<head>` section
2. Replace with your preferred fonts
3. Update the `font-family` declarations in CSS

---

## 📱 Using a Custom Domain

Want to use your own domain (e.g., `carryon.alysmalls.com`)?

1. **Buy a domain** (Namecheap, Google Domains, etc.)

2. **In GitHub Pages settings:**
   - Enter your custom domain
   - Check "Enforce HTTPS"

3. **In your domain registrar:**
   - Add a CNAME record pointing to `YOUR-USERNAME.github.io`

[Detailed GitHub Pages custom domain guide →](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)

---

## 🔄 Deployment Alternatives

While this README focuses on GitHub Pages, you can also deploy to:

### Cloudflare Pages
- Faster global CDN
- Unlimited bandwidth
- Free SSL
- [Deploy Guide](https://pages.cloudflare.com/)

### Netlify
- Drag-and-drop deployment
- Instant preview URLs
- Free SSL
- [Deploy Guide](https://www.netlify.com/)

All three options are **100% free** for static sites like this!

---

## 📝 Maintenance Schedule

**Recommended update frequency:**

- **Major Airlines** (United, Delta, American, Southwest, etc.): Check quarterly
- **International Airlines**: Check bi-annually
- **Budget Airlines**: Check quarterly (they change policies more often)
- **Luggage Library**: Add new bags as you test them

**Where to check for airline updates:**
- Official airline websites (baggage/carry-on policy pages)
- Set Google Alerts for "airline name + carry-on policy change"
- Aviation news sites and forums

---

## 🤝 Contributing

Found an airline with outdated dimensions? Tested a new bag?

1. Fork this repository
2. Make your changes to `airlines.json` or `luggage.json`
3. Submit a pull request with:
   - The airline/bag name
   - Link to the official source
   - Date you verified the information

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

Feel free to fork, modify, and use for your own projects!

---

## 🙏 Credits

- **Created by:** [Aly Smalls](https://likewhereyouregoing.com)
- **YouTube:** [@alysmalls](https://www.youtube.com/@alysmalls)
- **Design:** Inspired by Like Where You're Going blog aesthetic

---

## 💡 Future Enhancements (Ideas)

Want to take this further? Consider:

- [ ] Add airline logos/icons
- [ ] Filter airlines by region (US, Europe, Asia, etc.)
- [ ] Sort results by airline popularity
- [ ] Add "bookmark" feature to save favorite bags
- [ ] Include personal item dimensions
- [ ] Add weight restrictions
- [ ] Community submissions for bag reviews

---

## 🐛 Issues or Questions?

- Open an issue on GitHub
- Contact Aly via [her website](https://likewhereyouregoing.com/connect-with-me/)

---

**Happy travels! ✈️**

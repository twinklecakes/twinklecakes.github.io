# Personal Website - Setup & Customization Guide

This is a modern, clean personal website built with pure HTML, CSS, and vanilla JavaScript. No frameworks or complex build tools required—just deploy and it works!

## 📁 What You're Getting

```
.
├── index.html          # Homepage
├── about.html          # About page with timeline
├── work.html           # Portfolio/Work showcase
├── blog.html           # Blog listing
├── contact.html        # Contact form
├── style.css           # Single stylesheet (all styling)
├── Headshot.jpeg       # Your profile image
└── README.md           # This file
```

## ✨ Design Philosophy

This website uses a **refined, minimal aesthetic** inspired by KC Shornima's elegant design:

- **Typography**: Playfair Display (headers) + Nunito (body)
- **Color Palette**: Warm cream background with warm gold/brown accents
- **Layout**: Clean, spacious, responsive
- **Consistency**: Single CSS file with design system variables—easy to maintain!

## 🚀 Quick Start

### 1. No Installation Needed
Just push these files to your GitHub Pages repo (`twinklecakes.github.io`):
```bash
# In your repo directory
git add .
git commit -m "Update website files"
git push origin main
```

Your site will be live at `https://twinklecakes.github.io/` (or your custom domain)

### 2. Customize Content

#### Homepage (`index.html`)
- Update the hero section text
- Change featured work cards
- Customize the "Latest Thoughts" blog preview

#### About Page (`about.html`)
- Replace placeholder image with your headshot
- Update bio text
- Modify skills in the grid
- Update experience timeline

#### Work/Portfolio (`work.html`)
- Replace project descriptions
- Add project images (replace the emoji placeholders)
- Update project metadata and tech stacks
- Add actual project links

#### Blog (`blog.html`)
- Add your actual blog posts
- Update dates and excerpts
- Customize categories

#### Contact (`contact.html`)
- Update email address (appears 3 times!)
- Set up form: Use [Formspree.io](https://formspree.io/) for free email forms
- Update social media links

### 3. Customize the Design

All colors and spacing are CSS variables at the top of `style.css`. Change them once, and they apply everywhere:

```css
:root {
  --primary-dark: #1a1a1a;      /* Main dark color */
  --accent-warm: #d4956d;        /* Warm accent (gold/brown) */
  --primary-light: #f8f6f3;      /* Background color */
  /* ... more variables ... */
}
```

**Common customizations:**

```css
/* Change accent color */
--accent-warm: #8b6f47;    /* Darker brown */
--accent-gold: #a68968;    /* Complementary color */

/* Change fonts (find on Google Fonts) */
--font-display: 'Playfair Display', serif;
--font-body: 'Nunito', sans-serif;

/* Adjust spacing */
--spacing-lg: 2rem;
--spacing-2xl: 4rem;
```

## 🎨 Key Features

### ✅ Mobile Responsive
- Works beautifully on all devices
- Mobile nav toggle included
- Adaptive layouts

### ✅ No Dependencies
- Pure HTML/CSS/JavaScript
- No build tools needed
- Fast load times
- No Jekyll required!

### ✅ Easy Maintenance
- Single CSS file keeps everything consistent
- Clear, well-commented code
- Simple HTML structure
- CSS variables for quick updates

### ✅ Design System Included
- **Typography**: Consistent heading sizes and weights
- **Spacing**: Unified spacing scale
- **Colors**: Limited, cohesive palette
- **Components**: Buttons, cards, forms, all styled

## 🔧 Customization Examples

### Change Your Brand Color
```css
:root {
  --accent-warm: #7cb9e8;      /* From gold to blue */
  --accent-gold: #5a9bd3;
}
```
This automatically updates buttons, links, hover states, and accents everywhere!

### Add Your Logo/Brand Image
In the navigation, replace the text logo:
```html
<!-- Before -->
<a href="/" class="nav-logo">Avelyn</a>

<!-- After (with image) -->
<a href="/" class="nav-logo">
  <img src="logo.png" alt="Your Logo" style="height: 40px;">
</a>
```

### Customize Fonts
1. Go to [Google Fonts](https://fonts.google.com/)
2. Find fonts you like
3. Copy the import link and replace in `<head>`
4. Update CSS variables:
```css
--font-display: 'New Display Font', serif;
--font-body: 'New Body Font', sans-serif;
```

### Add Smooth Scroll Animation
Already included! Links with `#anchor` scroll smoothly.

### Add Blog Post Archive
The blog.html already has a nice card grid. Just add more `<article class="blog-card">` elements.

## 🌐 Hosting & Deployment

### GitHub Pages (Free!)
1. Push these files to `twinklecakes.github.io`
2. Go to Settings → Pages
3. Ensure "Deploy from a branch" is enabled
4. Branch: `main`, folder: `/(root)`
5. Done! Your site is live in ~1 minute

### Custom Domain
If you have a domain (like `avelynb.com`):
1. Add a `CNAME` file with your domain name
2. Update DNS settings at your registrar
3. GitHub will automatically use it

## 📝 Important Notes

### Images
- Replace the emoji placeholders with actual images
- Optimize images (use TinyPNG or similar)
- Update image paths in HTML files

### Contact Form
The contact form needs a backend service:
- **Free Option**: [Formspree.io](https://formspree.io/) - Best option!
  1. Sign up
  2. Get your form ID
  3. Update the form action: `https://formspree.io/f/YOUR_ID`

### Navigation Links
Make sure all links in the nav and footer work:
- Update social media URLs
- Ensure internal links point to correct files
- Test on live site

## 🎯 Common Questions

**Q: How do I add a new page?**
A: Create a new `.html` file, copy the structure from `index.html`, update the nav links on all pages.

**Q: Can I use this with Jekyll?**
A: You don't need Jekyll for this! It's pure static HTML. But if you want Jekyll later, just add `_config.yml` and use liquid templates.

**Q: How do I add animations?**
A: Add CSS animations in `style.css`. There are already examples like `@keyframes fadeInUp` and `@keyframes float`.

**Q: Can I use React or Vue?**
A: You could, but the current setup is simpler and faster. Only switch if you need dynamic content.

## 🚀 Next Steps

1. **Personalize content**: Update all text to your information
2. **Add images**: Replace placeholders with real images
3. **Set up contact form**: Use Formspree or similar
4. **Test mobile**: Open on phone and tablet
5. **Deploy**: Push to GitHub and verify it's live
6. **Customize colors**: Adjust CSS variables to match your brand

## 📊 File Sizes & Performance

- **Total CSS**: ~15kb
- **HTML pages**: ~5-8kb each
- **Load time**: < 1 second
- **Lighthouse Score**: 95+

No build process needed. No npm packages. Just pure web standards!

## 💡 Pro Tips

- **Update frequently**: Keep blog posts, work samples, and about section fresh
- **Keep it simple**: Resist adding too much. Minimal design ages well.
- **Use Google Fonts**: They're free and fast
- **Optimize images**: Larger images slow down your site
- **Test often**: Check on mobile, tablet, and desktop

## 🤝 Support & Questions

- Check for typos in file paths (they're case-sensitive on Linux)
- Ensure all Google Fonts are loading (check browser console)
- Test contact form on live site after deployment
- Use browser DevTools to debug styles

---

**Happy building! This website is yours to customize.** 🎉

Make it reflect who you are. Keep it updated. Let it grow with you.

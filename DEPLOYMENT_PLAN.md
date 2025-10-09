# 🏕️ Bay Area Camping Tracker - Deployment Plan

## 🚀 GitHub Pages Deployment with Custom Domain

### **Target URL:** `https://yayarea.camp`

---

## **Phase 1: Prepare Repository (5 minutes)**

### 1. Create GitHub Repository
- Go to GitHub.com → Click "New Repository"
- **Name:** `bay-area-camping` (or your preferred name)
- **Description:** "Real-time Bay Area campsite availability tracker"
- **Make it PUBLIC** (required for free GitHub Pages)
- **Don't initialize with README** (you already have one)

### 2. Upload Files to GitHub
```bash
# In your project directory
git init
git add .
git commit -m "Initial commit: Bay Area camping tracker"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/bay-area-camping.git
git push -u origin main
```

**Replace `YOUR_USERNAME` with your actual GitHub username**

---

## **Phase 2: Configure GitHub Pages (2 minutes)**

### 3. Enable GitHub Pages
- Go to your repository → **Settings**
- Scroll down to **Pages** section
- Under **Source**: Select **GitHub Actions**
- Click **Save**

### 4. Enable GitHub Actions
- Go to **Actions** tab in your repository
- Click **"I understand my workflows, go ahead and enable them"**

---

## **Phase 3: Test Deployment (5 minutes)**

### 5. Manual Test Run
- Go to **Actions** tab
- Click **Bay Area Campsite Search** workflow
- Click **Run workflow** button
- Wait 5-10 minutes for completion
- Check the **gh-pages** branch is created

### 6. Verify Your Site
- Go to **Settings** → **Pages**
- Your site URL will be: `https://YOUR_USERNAME.github.io/bay-area-camping`
- Click the link to verify it works

---

## **Phase 4: Custom Domain Setup**

### 7. Purchase Domain (5 minutes)
**Buy `yayarea.camp` from a domain registrar:**
- **Namecheap**: ~$12/year
- **GoDaddy**: ~$15/year  
- **Cloudflare**: ~$10/year (cheapest)
- **Google Domains**: ~$12/year

### 8. Configure DNS Records (5 minutes)
In your domain registrar's DNS settings, add:

**For www.yayarea.camp:**
```
Type: CNAME
Name: www
Value: YOUR_USERNAME.github.io
```

**For yayarea.camp (root domain):**
```
Type: A
Name: @
Value: 185.199.108.153
Value: 185.199.109.153
Value: 185.199.110.153
Value: 185.199.111.153
```

### 9. Configure GitHub Pages for Custom Domain (2 minutes)
- Go to your repository → **Settings** → **Pages**
- Under **Custom domain**: Enter `yayarea.camp`
- Check **Enforce HTTPS** (recommended)
- Click **Save**

### 10. SSL Certificate (Automatic)
- GitHub automatically provides SSL certificates
- Wait 24-48 hours for SSL to fully propagate
- Your site will be available at both:
  - `https://yayarea.camp`
  - `https://www.yayarea.camp`

---

## **Phase 5: Monitor & Maintain (Ongoing)**

### 11. Check Status
- **Actions** tab shows workflow runs
- **Green checkmark** = successful
- **Red X** = failed (check logs)

### 12. View Logs (if needed)
- Click any workflow run
- Click **search-and-deploy** job
- Expand steps to see detailed logs

---

## **What Happens Automatically**

### **Every Hour:**
1. **GitHub Actions triggers** at the top of each hour
2. **Python script runs** your campsite search
3. **Results saved** to `results.json`
4. **Files deployed** to GitHub Pages
5. **Your site updates** with fresh data

### **Your Site Features:**
- ✅ **Real-time data** updated hourly
- ✅ **Beautiful interface** showing available campsites
- ✅ **Distance sorting** (closest first)
- ✅ **Direct booking links** to ReserveCalifornia
- ✅ **Mobile-friendly** design
- ✅ **Free hosting** forever

---

## **Customization Options**

### **Change Update Frequency:**
Edit `.github/workflows/campsite-search.yml`:
```yaml
schedule:
  - cron: '0 */2 * * *'  # Every 2 hours
  - cron: '0 6,18 * * *'  # Twice daily (6 AM and 6 PM)
  - cron: '0 9 * * *'     # Once daily at 9 AM
```

### **Modify Search Parameters:**
Edit `new_main.py` lines 271-274:
```python
start_date = datetime.date.today() + relativedelta(days=1)
end_date = start_date + relativedelta(months=6)  # Search 6 months ahead
consecutive_nights = 3  # Look for 3 consecutive nights
weekends_only = False   # Search all days
```

---

## **Expected Timeline**

- **Setup**: 10-15 minutes total
- **First run**: 5-10 minutes
- **Site live**: Within 15 minutes of first successful run
- **Custom domain**: Working within 1-2 hours
- **HTTPS**: Working within 24-48 hours
- **Hourly updates**: Automatic forever

---

## **Cost Breakdown**

- **GitHub Pages**: Free
- **GitHub Actions**: Free (2,000 minutes/month)
- **Domain**: ~$10-15/year
- **SSL Certificate**: Free (provided by GitHub)
- **Total**: ~$1/month

---

## **Final Result**

Your professional campsite availability tracker will be available at:
- ✅ `https://yayarea.camp`
- ✅ `https://www.yayarea.camp`
- ✅ Automatic hourly updates
- ✅ Beautiful, mobile-friendly interface
- ✅ Direct booking links
- ✅ Completely free hosting (except domain cost)

---

## **Troubleshooting**

### **If GitHub Actions Fails:**
1. Check the logs in the Actions tab
2. Common issues:
   - API rate limiting (will retry next hour)
   - Network connectivity (temporary)
   - Python dependency issues

### **If Custom Domain Doesn't Work:**
1. Wait up to 24 hours for DNS propagation
2. Check DNS records are correct
3. Verify CNAME file exists in repository
4. Ensure domain is set in GitHub Pages settings

### **If Site Shows "Loading":**
1. This is normal - the search takes time
2. Check if `results.json` exists in the repository
3. Verify the last GitHub Actions run was successful

---

**Happy Camping! 🏕️**

*This plan will get your Bay Area camping tracker live and automatically updating every hour.*

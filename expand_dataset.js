const fs = require('fs');
const path = require('path');

const platforms = ['Twitter/X', 'Instagram', 'LinkedIn', 'Reddit', 'YouTube'];
const contentTypes = ['Text', 'Image', 'Video', 'Carousel', 'Poll', 'Link'];
const scrapers = ['BeautifulSoup + Requests', 'Selenium WebDriver', 'Snscrape', 'PRAW (Python Reddit API)', 'Tweepy / API Scraper'];

const authors = [
  { username: '@tech_insights', followers: 24500 },
  { username: '@ai_daily', followers: 89000 },
  { username: '@dev_chronicles', followers: 15300 },
  { username: '@code_craftsman', followers: 32000 },
  { username: '@future_of_work', followers: 56000 },
  { username: '@data_nerd_99', followers: 12400 },
  { username: '@cloud_architect', followers: 41000 },
  { username: '@startup_digest', followers: 67800 },
  { username: '@marketing_pulse', followers: 28900 },
  { username: '@cyber_guardian', followers: 19800 },
  { username: '@uiux_designer', followers: 34200 },
  { username: '@python_ninja', followers: 75000 },
  { username: '@ml_engineer', followers: 48500 },
  { username: '@growth_hacker', followers: 52100 },
  { username: '@bigdata_pro', followers: 61000 }
];

const postTemplates = [
  {
    text: "Excited to share our new automated data pipeline built using Python and FastAPI! Scaled to 10M records effortlessly. #Python #DataEngineering #Cloud",
    sentiment: 0.78, category: "Positive", subj: 0.65, tags: "#Python, #DataEngineering, #Cloud", mentions: "@CloudTech", type: "Image"
  },
  {
    text: "Debugging legacy distributed systems on a Sunday night is always a humbling experience. Finally fixed the concurrency race condition. #SoftwareEngineering #DevLife",
    sentiment: 0.12, category: "Neutral", subj: 0.40, tags: "#SoftwareEngineering, #DevLife", mentions: "None", type: "Text"
  },
  {
    text: "Deep Learning models are revolutionizing computer vision, but model interpretability remains a critical challenge in medical applications. #AI #DeepLearning #Healthcare",
    sentiment: 0.45, category: "Positive", subj: 0.55, tags: "#AI, #DeepLearning, #Healthcare", mentions: "@HealthAI", type: "Link"
  },
  {
    text: "Frustrated with the recent API rate limits and breaking changes introduced without prior notice. Down for 3 hours! #TechRant #API #DevOps",
    sentiment: -0.72, category: "Negative", subj: 0.85, tags: "#TechRant, #API, #DevOps", mentions: "@CloudHost", type: "Text"
  },
  {
    text: "Here is our comprehensive guide to mastering Exploratory Data Analysis in Python using Pandas, Seaborn and Plotly. Check the repo below! #DataScience #Python #EDA",
    sentiment: 0.82, category: "Positive", subj: 0.60, tags: "#DataScience, #Python, #EDA", mentions: "@DataWorld", type: "Carousel"
  },
  {
    text: "Remote work productivity survey results: 74% engineers prefer hybrid over 5 days in-office. Flexibility drives innovation. #FutureOfWork #WorkplaceTrends",
    sentiment: 0.55, category: "Positive", subj: 0.48, tags: "#FutureOfWork, #WorkplaceTrends", mentions: "@HRInsights", type: "Poll"
  },
  {
    text: "Is Kubernetes overkill for small to medium scale microservices? Join our live discussion today. #DevOps #Kubernetes #Docker",
    sentiment: 0.05, category: "Neutral", subj: 0.35, tags: "#DevOps, #Kubernetes, #Docker", mentions: "None", type: "Video"
  },
  {
    text: "System outage alert: Major cloud region experiencing elevated latency and 504 gateway errors. Investigation in progress. #CloudAlert #DevOps #SRE",
    sentiment: -0.58, category: "Negative", subj: 0.30, tags: "#CloudAlert, #DevOps, #SRE", mentions: "@CloudStatus", type: "Text"
  },
  {
    text: "Honored to receive the Best Innovation Award for our real-time social sentiment dashboard at the National Tech Summit! #Achievement #AI #Innovation",
    sentiment: 0.92, category: "Positive", subj: 0.75, tags: "#Achievement, #AI, #Innovation", mentions: "@TechSummit", type: "Image"
  },
  {
    text: "Top 5 SQL optimization tricks every backend developer must know to reduce query latency by 80%. Bookmark this thread! #SQL #Database #Backend",
    sentiment: 0.68, category: "Positive", subj: 0.50, tags: "#SQL, #Database, #Backend", mentions: "None", type: "Carousel"
  },
  {
    text: "Why do so many AI startups just wrap OpenAI API without building proprietary defensive moats? Thoughts? #AI #Startups #VentureCapital",
    sentiment: -0.25, category: "Negative", subj: 0.60, tags: "#AI, #Startups, #VentureCapital", mentions: "@TechReview", type: "Text"
  },
  {
    text: "Just published a comprehensive tutorial on building end-to-end sentiment analytics dashboards using Streamlit, VADER and Plotly! #Python #Streamlit #DataViz",
    sentiment: 0.85, category: "Positive", subj: 0.62, tags: "#Python, #Streamlit, #DataViz", mentions: "@StreamlitDev", type: "Video"
  },
  {
    text: "Comparing transformer architectures: BERT vs RoBERTa vs DeBERTa for domain-specific NLP classification tasks. Benchmark results inside. #NLP #MachineLearning",
    sentiment: 0.38, category: "Positive", subj: 0.42, tags: "#NLP, #MachineLearning", mentions: "@HuggingFace", type: "Link"
  },
  {
    text: "Terrible customer experience with the cloud migration support team today. Tickets left unanswered for over 12 hours. Very disappointed. #CloudSupport #Fail",
    sentiment: -0.81, category: "Negative", subj: 0.90, tags: "#CloudSupport, #Fail", mentions: "@CloudCare", type: "Text"
  },
  {
    text: "Web scraping ethical practices: Always obey robots.txt, implement rate limiting, and cache responses to avoid hammering servers. #WebScraping #Python",
    sentiment: 0.48, category: "Positive", subj: 0.52, tags: "#WebScraping, #Python", mentions: "None", type: "Text"
  },
  {
    text: "Analyzing 100,000 Reddit comments to uncover consumer sentiment trends around generative AI tools in 2026. Fascinating patterns emerged! #Analytics #GenAI #Data",
    sentiment: 0.74, category: "Positive", subj: 0.58, tags: "#Analytics, #GenAI, #Data", mentions: "@DataTrends", type: "Image"
  },
  {
    text: "Micro-frontends architecture: Is the team autonomy gain worth the build and deployment overhead? Our experience after 1 year. #WebDev #Architecture",
    sentiment: 0.08, category: "Neutral", subj: 0.38, tags: "#WebDev, #Architecture", mentions: "None", type: "Link"
  },
  {
    text: "Major security vulnerability discovered in popular npm package with 5M weekly downloads. Patch immediately! CVE-2026-9812 #CyberSecurity #InfoSec",
    sentiment: -0.66, category: "Negative", subj: 0.40, tags: "#CyberSecurity, #InfoSec", mentions: "@SecTeam", type: "Text"
  },
  {
    text: "Clean Code principles applied to Python data science workflows: Write functions, use type hints, and write modular unit tests. #CleanCode #Python",
    sentiment: 0.62, category: "Positive", subj: 0.50, tags: "#CleanCode, #Python", mentions: "None", type: "Carousel"
  },
  {
    text: "Quarterly earnings report reflects strong adoption of enterprise SaaS solutions with 35% YoY expansion. Consistent sustainable growth. #FinTech #Business",
    sentiment: 0.71, category: "Positive", subj: 0.45, tags: "#FinTech, #Business", mentions: "@MarketWatch", type: "Image"
  }
];

function cleanText(txt) {
  return txt.toLowerCase()
    .replace(/https?:\/\/\S+/g, '')
    .replace(/#\w+/g, '')
    .replace(/@\w+/g, '')
    .replace(/[^a-z0-9\s]/g, '')
    .replace(/\s+/g, ' ')
    .trim();
}

function escapeCsv(val) {
  if (val === null || val === undefined) return '""';
  const str = String(val);
  if (str.includes(',') || str.includes('"') || str.includes('\n')) {
    return `"${str.replace(/"/g, '""')}"`;
  }
  return str;
}

const header = [
  'post_id', 'platform', 'post_url', 'author_username', 'author_followers_count',
  'post_timestamp', 'post_text', 'cleaned_text', 'content_type', 'language',
  'likes_count', 'comments_count', 'shares_count', 'views_count', 'engagement_rate',
  'sentiment_score', 'sentiment_category', 'subjectivity_score', 'hashtags',
  'hashtags_count', 'mentions', 'character_count', 'word_count', 'scraped_timestamp',
  'scraper_module'
];

const rows = [header.join(',')];

// 500 rows
for (let i = 1; i <= 500; i++) {
  const tpl = postTemplates[(i - 1) % postTemplates.length];
  const author = authors[(i - 1) % authors.length];
  const platform = platforms[(i * 3) % platforms.length];
  const scraper = scrapers[(i * 2) % scrapers.length];
  
  const postId = `PST_${1048000 + i}`;
  const slug = platform.toLowerCase().replace(/[^a-z]/g, '');
  const postUrl = `https://${slug}.com/${author.username.replace('@','')}/status/${178920000 + i * 17}`;
  
  const day = (i % 28) + 1;
  const hour = (i * 7) % 24;
  const min = (i * 13) % 60;
  const sec = (i * 19) % 60;
  const postTime = `2026-10-${String(day).padStart(2, '0')} ${String(hour).padStart(2, '0')}:${String(min).padStart(2, '0')}:${String(sec).padStart(2, '0')}`;
  
  const scrapedDay = Math.min(30, day + 1);
  const scrapedTime = `2026-10-${String(scrapedDay).padStart(2, '0')} 11:25:30`;
  
  const multiplier = Math.floor(author.followers / 2000) + 5;
  const likes = (i * 47 * multiplier) % 5200 + 45;
  const comments = Math.floor(likes * (0.08 + (i % 10) * 0.015)) + 5;
  const shares = Math.floor(likes * (0.05 + (i % 7) * 0.02)) + 2;
  const views = Math.max(likes * 12 + 500, likes + comments + shares + 400 + (i * 35));
  const engRate = (((likes + comments + shares) / views) * 100).toFixed(2);
  
  const cleaned = cleanText(tpl.text);
  const words = tpl.text.split(/\s+/).length;
  const chars = tpl.text.length;
  const tagList = tpl.tags === 'None' ? [] : tpl.tags.split(',').map(s => s.trim());
  
  const rowData = [
    postId,
    platform,
    postUrl,
    author.username,
    author.followers,
    postTime,
    tpl.text,
    cleaned,
    tpl.type,
    'en',
    likes,
    comments,
    shares,
    views,
    engRate,
    tpl.sentiment.toFixed(2),
    tpl.category,
    tpl.subj.toFixed(2),
    tpl.tags,
    tagList.length,
    tpl.mentions,
    chars,
    words,
    scrapedTime,
    scraper
  ];
  
  rows.push(rowData.map(escapeCsv).join(','));
}

const csvOutput = rows.join('\r\n');

const outPath1 = path.join('d:', 'My Portfolio', 'dataset.csv');
const outPath2 = path.join('d:', 'My Portfolio', '06_Social_Media_Analytics_Dashboard', 'dataset.csv');

fs.writeFileSync(outPath1, csvOutput, 'utf-8');
fs.writeFileSync(outPath2, csvOutput, 'utf-8');

console.log('Successfully generated 500-record dataset.csv');

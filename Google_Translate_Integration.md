# Google Translate Integration Guide

## Overview

This document provides detailed implementation guidelines for integrating Google Cloud Translation API into the AI-Based Multilingual Quiz Platform.

## Table of Contents

1. [Setup & Configuration](#setup--configuration)
2. [Authentication](#authentication)
3. [API Usage](#api-usage)
4. [Caching Strategy](#caching-strategy)
5. [Cost Optimization](#cost-optimization)
6. [Error Handling](#error-handling)
7. [Best Practices](#best-practices)

---

## Setup & Configuration

### Prerequisites

1. **Google Cloud Account**
   - Create a project at [Google Cloud Console](https://console.cloud.google.com)
   - Enable Cloud Translation API
   - Create service account credentials

2. **API Credentials**
   ```bash
   # Download service account JSON key
   # Store securely as environment variable or in secrets manager
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
   export GOOGLE_CLOUD_PROJECT_ID="your-project-id"
   ```

3. **Install SDK**
   ```bash
   # Python
   pip install google-cloud-translate==3.12.0
   
   # Node.js
   npm install @google-cloud/translate@8.0.0
   ```

### Configuration

```javascript
// config/translation.js
module.exports = {
  google: {
    projectId: process.env.GOOGLE_CLOUD_PROJECT_ID,
    credentials: process.env.GOOGLE_APPLICATION_CREDENTIALS,
    location: 'global', // or specific region like 'us-central1'
  },
  cache: {
    enabled: true,
    ttl: {
      permanent: null, // UI elements
      longTerm: 2592000, // 30 days - quiz content
      mediumTerm: 604800, // 7 days - user content
      shortTerm: 3600, // 1 hour - temporary
    },
  },
  rateLimiting: {
    maxRequestsPerMinute: 50,
    maxCharactersPerMinute: 100000,
  },
  batching: {
    enabled: true,
    maxBatchSize: 100,
    maxBatchWaitTime: 100, // milliseconds
  },
};
```

---

## Authentication

### Service Account Method (Recommended for Production)

```python
# Python implementation
from google.cloud import translate_v3
from google.oauth2 import service_account

class TranslationClient:
    def __init__(self, credentials_path, project_id):
        self.credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
        self.client = translate_v3.TranslationServiceClient(
            credentials=self.credentials
        )
        self.project_id = project_id
        self.location = 'global'
        self.parent = f"projects/{project_id}/locations/{self.location}"
```

### API Key Method (For Development)

```javascript
// Node.js implementation
const { Translate } = require('@google-cloud/translate').v2;

class TranslationClient {
  constructor(apiKey) {
    this.translate = new Translate({
      key: apiKey,
    });
  }
  
  async translate(text, target) {
    const [translation] = await this.translate.translate(text, target);
    return translation;
  }
}
```

---

## API Usage

### Basic Translation

```python
# Python - Single text translation
def translate_text(text, target_language, source_language='auto'):
    """
    Translate text to target language
    
    Args:
        text: Text to translate
        target_language: ISO 639-1 language code (e.g., 'es', 'fr', 'de')
        source_language: Source language code (optional, auto-detect if not provided)
    
    Returns:
        Translated text string
    """
    request = {
        'parent': self.parent,
        'contents': [text],
        'target_language_code': target_language,
        'mime_type': 'text/plain'
    }
    
    if source_language != 'auto':
        request['source_language_code'] = source_language
    
    response = self.client.translate_text(request=request)
    return response.translations[0].translated_text
```

```javascript
// Node.js - Single text translation
async translateText(text, targetLanguage, sourceLanguage = null) {
  const options = {
    to: targetLanguage,
  };
  
  if (sourceLanguage) {
    options.from = sourceLanguage;
  }
  
  const [translation] = await this.translate.translate(text, options);
  return translation;
}
```

### Batch Translation

```python
# Python - Batch translation for efficiency
def batch_translate(texts, target_language, source_language='auto'):
    """
    Translate multiple texts in a single API call
    
    Args:
        texts: List of text strings to translate
        target_language: Target language code
        source_language: Source language code (optional)
    
    Returns:
        List of translated text strings
    """
    # Google Translate API supports up to 100 texts per request
    request = {
        'parent': self.parent,
        'contents': texts[:100],  # Limit to 100
        'target_language_code': target_language,
        'mime_type': 'text/plain'
    }
    
    if source_language != 'auto':
        request['source_language_code'] = source_language
    
    response = self.client.translate_text(request=request)
    return [t.translated_text for t in response.translations]
```

```javascript
// Node.js - Batch translation
async batchTranslate(texts, targetLanguage, sourceLanguage = null) {
  const options = {
    to: targetLanguage,
  };
  
  if (sourceLanguage) {
    options.from = sourceLanguage;
  }
  
  const [translations] = await this.translate.translate(texts, options);
  
  // Ensure we always return an array
  return Array.isArray(translations) ? translations : [translations];
}
```

### Language Detection

```python
# Python - Detect source language
def detect_language(text):
    """
    Detect the language of the input text
    
    Args:
        text: Text to analyze
    
    Returns:
        Language code and confidence score
    """
    request = {
        'parent': self.parent,
        'content': text,
        'mime_type': 'text/plain'
    }
    
    response = self.client.detect_language(request=request)
    
    # Return the most confident language
    languages = response.languages
    if languages:
        return {
            'language': languages[0].language_code,
            'confidence': languages[0].confidence
        }
    return None
```

```javascript
// Node.js - Language detection
async detectLanguage(text) {
  const [detection] = await this.translate.detect(text);
  return {
    language: detection.language,
    confidence: detection.confidence,
  };
}
```

### Get Supported Languages

```python
# Python - Get list of supported languages
def get_supported_languages(display_language='en'):
    """
    Get list of all supported languages
    
    Args:
        display_language: Language code for language names
    
    Returns:
        List of supported language codes and names
    """
    request = {
        'parent': self.parent,
        'display_language_code': display_language
    }
    
    response = self.client.get_supported_languages(request=request)
    
    return [
        {
            'code': lang.language_code,
            'name': lang.display_name
        }
        for lang in response.languages
    ]
```

---

## Caching Strategy

### Cache Implementation

```python
# Python - Redis caching for translations
import redis
import hashlib
import json

class TranslationCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.prefix = 'trans:'
    
    def _generate_key(self, text, source_lang, target_lang):
        """Generate consistent cache key"""
        text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
        return f"{self.prefix}{source_lang}:{target_lang}:{text_hash}"
    
    async def get(self, text, source_lang, target_lang):
        """Get cached translation"""
        key = self._generate_key(text, source_lang, target_lang)
        cached = await self.redis.get(key)
        
        if cached:
            data = json.loads(cached)
            # Update access count and last accessed time
            await self.redis.hincrby(f"{key}:meta", 'access_count', 1)
            await self.redis.hset(f"{key}:meta", 'last_accessed', time.time())
            return data['translation']
        
        return None
    
    async def set(self, text, source_lang, target_lang, translation, ttl=None):
        """Cache translation with optional TTL"""
        key = self._generate_key(text, source_lang, target_lang)
        
        data = {
            'text': text,
            'source_lang': source_lang,
            'target_lang': target_lang,
            'translation': translation,
            'cached_at': time.time()
        }
        
        # Store translation
        await self.redis.set(key, json.dumps(data), ex=ttl)
        
        # Store metadata
        meta = {
            'access_count': 1,
            'created_at': time.time(),
            'last_accessed': time.time()
        }
        await self.redis.hmset(f"{key}:meta", meta)
```

```javascript
// Node.js - Redis caching for translations
const crypto = require('crypto');

class TranslationCache {
  constructor(redisClient) {
    this.redis = redisClient;
    this.prefix = 'trans:';
  }
  
  _generateKey(text, sourceLang, targetLang) {
    const textHash = crypto
      .createHash('md5')
      .update(text)
      .digest('hex');
    return `${this.prefix}${sourceLang}:${targetLang}:${textHash}`;
  }
  
  async get(text, sourceLang, targetLang) {
    const key = this._generateKey(text, sourceLang, targetLang);
    const cached = await this.redis.get(key);
    
    if (cached) {
      const data = JSON.parse(cached);
      
      // Update metadata
      await this.redis.hincrby(`${key}:meta`, 'access_count', 1);
      await this.redis.hset(`${key}:meta`, 'last_accessed', Date.now());
      
      return data.translation;
    }
    
    return null;
  }
  
  async set(text, sourceLang, targetLang, translation, ttl = null) {
    const key = this._generateKey(text, sourceLang, targetLang);
    
    const data = {
      text,
      source_lang: sourceLang,
      target_lang: targetLang,
      translation,
      cached_at: Date.now()
    };
    
    // Store translation
    if (ttl) {
      await this.redis.setex(key, ttl, JSON.stringify(data));
    } else {
      await this.redis.set(key, JSON.stringify(data));
    }
    
    // Store metadata
    await this.redis.hmset(`${key}:meta`, {
      access_count: 1,
      created_at: Date.now(),
      last_accessed: Date.now()
    });
  }
}
```

### Cache Strategy by Content Type

```javascript
const CACHE_TTL = {
  // UI elements (permanent)
  ui: null,
  
  // Quiz content (30 days)
  quiz: 30 * 24 * 60 * 60,
  
  // Questions (30 days)
  question: 30 * 24 * 60 * 60,
  
  // User-generated content (7 days)
  user_content: 7 * 24 * 60 * 60,
  
  // Temporary content (1 hour)
  temp: 60 * 60,
};

function getCacheTTL(contentType) {
  return CACHE_TTL[contentType] || CACHE_TTL.temp;
}
```

---

## Cost Optimization

### Request Batching

```javascript
// Batching manager to combine multiple translation requests
class BatchTranslationManager {
  constructor(translationClient, options = {}) {
    this.client = translationClient;
    this.maxBatchSize = options.maxBatchSize || 100;
    this.maxWaitTime = options.maxWaitTime || 100; // ms
    this.pendingBatches = new Map();
  }
  
  async translate(text, targetLang, sourceLang = 'auto') {
    const batchKey = `${sourceLang}:${targetLang}`;
    
    return new Promise((resolve, reject) => {
      if (!this.pendingBatches.has(batchKey)) {
        this.pendingBatches.set(batchKey, {
          texts: [],
          resolvers: [],
          timer: null
        });
      }
      
      const batch = this.pendingBatches.get(batchKey);
      batch.texts.push(text);
      batch.resolvers.push({ resolve, reject });
      
      // Clear existing timer
      if (batch.timer) {
        clearTimeout(batch.timer);
      }
      
      // Execute batch if it reaches max size
      if (batch.texts.length >= this.maxBatchSize) {
        this._executeBatch(batchKey);
      } else {
        // Otherwise, wait for more requests
        batch.timer = setTimeout(() => {
          this._executeBatch(batchKey);
        }, this.maxWaitTime);
      }
    });
  }
  
  async _executeBatch(batchKey) {
    const batch = this.pendingBatches.get(batchKey);
    this.pendingBatches.delete(batchKey);
    
    if (!batch || batch.texts.length === 0) return;
    
    const [sourceLang, targetLang] = batchKey.split(':');
    
    try {
      const translations = await this.client.batchTranslate(
        batch.texts,
        targetLang,
        sourceLang === 'auto' ? null : sourceLang
      );
      
      // Resolve all promises
      batch.resolvers.forEach((resolver, index) => {
        resolver.resolve(translations[index]);
      });
    } catch (error) {
      // Reject all promises
      batch.resolvers.forEach(resolver => {
        resolver.reject(error);
      });
    }
  }
}
```

### Usage Monitoring

```python
# Python - Track API usage and costs
class UsageMonitor:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.cost_per_char = 0.00002  # $20 per 1M characters
    
    async def track_request(self, char_count, target_lang):
        """Track translation request"""
        date_key = datetime.now().strftime('%Y-%m-%d')
        
        # Track character count
        await self.redis.hincrby(f"usage:{date_key}", 'chars', char_count)
        await self.redis.hincrby(f"usage:{date_key}", 'requests', 1)
        
        # Track by language
        await self.redis.hincrby(
            f"usage:{date_key}:lang",
            target_lang,
            char_count
        )
        
        # Calculate estimated cost
        total_chars = await self.redis.hget(f"usage:{date_key}", 'chars')
        estimated_cost = int(total_chars) * self.cost_per_char
        
        return {
            'chars_today': int(total_chars),
            'estimated_cost_today': estimated_cost
        }
    
    async def get_daily_report(self, date=None):
        """Get usage report for a specific date"""
        date_key = date or datetime.now().strftime('%Y-%m-%d')
        
        data = await self.redis.hgetall(f"usage:{date_key}")
        lang_data = await self.redis.hgetall(f"usage:{date_key}:lang")
        
        return {
            'date': date_key,
            'total_characters': int(data.get('chars', 0)),
            'total_requests': int(data.get('requests', 0)),
            'estimated_cost': int(data.get('chars', 0)) * self.cost_per_char,
            'by_language': {k: int(v) for k, v in lang_data.items()}
        }
```

---

## Error Handling

### Comprehensive Error Handler

```python
# Python - Error handling for translation service
from google.api_core import exceptions as google_exceptions
import time

class TranslationErrorHandler:
    def __init__(self, max_retries=3, backoff_factor=2):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
    
    async def handle_translation(self, func, *args, **kwargs):
        """
        Execute translation with error handling and retries
        """
        for attempt in range(self.max_retries):
            try:
                return await func(*args, **kwargs)
                
            except google_exceptions.ResourceExhausted as e:
                # Quota exceeded
                if attempt < self.max_retries - 1:
                    # Wait before retry
                    wait_time = self.backoff_factor ** attempt
                    await asyncio.sleep(wait_time)
                    continue
                else:
                    # Return cached or fallback
                    return await self._handle_quota_exceeded(*args, **kwargs)
            
            except google_exceptions.InvalidArgument as e:
                # Invalid input (language code, malformed text, etc.)
                return await self._handle_invalid_input(e, *args, **kwargs)
            
            except google_exceptions.PermissionDenied as e:
                # Authentication issue
                raise TranslationAuthError("Authentication failed") from e
            
            except google_exceptions.DeadlineExceeded as e:
                # Request timeout
                if attempt < self.max_retries - 1:
                    continue
                return await self._handle_timeout(*args, **kwargs)
            
            except Exception as e:
                # Unknown error
                return await self._handle_unknown_error(e, *args, **kwargs)
    
    async def _handle_quota_exceeded(self, text, target_lang, source_lang):
        """Handle quota exceeded - use cache or queue"""
        # Try to get from cache
        cached = await self.cache.get(text, source_lang, target_lang)
        if cached:
            return cached
        
        # Queue for later processing
        await self.queue.add({
            'text': text,
            'target_lang': target_lang,
            'source_lang': source_lang,
            'priority': 'low'
        })
        
        # Return original text as fallback
        return {
            'text': text,
            'translated': text,
            'error': 'QUOTA_EXCEEDED',
            'fallback': True
        }
    
    async def _handle_invalid_input(self, error, text, target_lang, source_lang):
        """Handle invalid input - try fallback language"""
        # Try translating to English as fallback
        if target_lang != 'en':
            try:
                return await self.translate(text, 'en', source_lang)
            except:
                pass
        
        return {
            'text': text,
            'translated': text,
            'error': 'INVALID_INPUT',
            'fallback': True
        }
    
    async def _handle_timeout(self, text, target_lang, source_lang):
        """Handle timeout - return cached or original"""
        cached = await self.cache.get(text, source_lang, target_lang)
        if cached:
            return cached
        
        return {
            'text': text,
            'translated': text,
            'error': 'TIMEOUT',
            'fallback': True
        }
```

```javascript
// Node.js - Error handling wrapper
class TranslationErrorHandler {
  constructor(client, cache, options = {}) {
    this.client = client;
    this.cache = cache;
    this.maxRetries = options.maxRetries || 3;
    this.backoffFactor = options.backoffFactor || 2;
  }
  
  async translateWithErrorHandling(text, targetLang, sourceLang = 'auto') {
    for (let attempt = 0; attempt < this.maxRetries; attempt++) {
      try {
        // Try cache first
        const cached = await this.cache.get(text, sourceLang, targetLang);
        if (cached) return cached;
        
        // Perform translation
        const result = await this.client.translate(text, targetLang, sourceLang);
        
        // Cache the result
        await this.cache.set(text, sourceLang, targetLang, result);
        
        return result;
        
      } catch (error) {
        // Handle specific error types
        if (error.code === 429 || error.message.includes('quota')) {
          // Quota exceeded
          if (attempt < this.maxRetries - 1) {
            await this.sleep(this.backoffFactor ** attempt * 1000);
            continue;
          }
          return this.handleQuotaExceeded(text, targetLang);
          
        } else if (error.code === 400) {
          // Invalid input
          return this.handleInvalidInput(text, targetLang, error);
          
        } else if (error.code === 504 || error.message.includes('timeout')) {
          // Timeout
          if (attempt < this.maxRetries - 1) {
            continue;
          }
          return this.handleTimeout(text, targetLang);
          
        } else {
          // Unknown error
          console.error('Translation error:', error);
          return this.handleUnknownError(text, error);
        }
      }
    }
  }
  
  handleQuotaExceeded(text, targetLang) {
    return {
      original: text,
      translated: text,
      error: 'QUOTA_EXCEEDED',
      fallback: true,
      message: 'Translation quota exceeded. Using original text.'
    };
  }
  
  handleInvalidInput(text, targetLang, error) {
    return {
      original: text,
      translated: text,
      error: 'INVALID_INPUT',
      fallback: true,
      message: `Invalid input: ${error.message}`
    };
  }
  
  handleTimeout(text, targetLang) {
    return {
      original: text,
      translated: text,
      error: 'TIMEOUT',
      fallback: true,
      message: 'Translation request timed out.'
    };
  }
  
  handleUnknownError(text, error) {
    return {
      original: text,
      translated: text,
      error: 'UNKNOWN_ERROR',
      fallback: true,
      message: `Translation failed: ${error.message}`
    };
  }
  
  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
```

---

## Best Practices

### 1. Always Use Caching

```javascript
// ✓ Good - Check cache first
async function translate(text, targetLang) {
  const cached = await cache.get(text, targetLang);
  if (cached) return cached;
  
  const result = await translateAPI(text, targetLang);
  await cache.set(text, targetLang, result);
  return result;
}

// ✗ Bad - Always call API
async function translate(text, targetLang) {
  return await translateAPI(text, targetLang);
}
```

### 2. Batch Similar Requests

```javascript
// ✓ Good - Batch multiple translations
const texts = ['Hello', 'World', 'Goodbye'];
const translations = await batchTranslate(texts, 'es');

// ✗ Bad - Individual requests
const translations = await Promise.all(
  texts.map(text => translate(text, 'es'))
);
```

### 3. Handle Errors Gracefully

```javascript
// ✓ Good - Fallback to original
try {
  return await translate(text, targetLang);
} catch (error) {
  console.error('Translation failed:', error);
  return text; // Return original text
}

// ✗ Bad - Throw error to user
return await translate(text, targetLang); // May crash app
```

### 4. Monitor Usage

```javascript
// ✓ Good - Track API usage
async function translate(text, targetLang) {
  const result = await translateAPI(text, targetLang);
  await usageMonitor.track(text.length, targetLang);
  return result;
}
```

### 5. Preserve Context

```python
# ✓ Good - Preserve formatting
def translate_with_formatting(html_text, target_lang):
    # Extract text from HTML
    soup = BeautifulSoup(html_text, 'html.parser')
    texts = [elem.text for elem in soup.find_all(text=True)]
    
    # Translate
    translations = batch_translate(texts, target_lang)
    
    # Rebuild HTML with translations
    for elem, translation in zip(soup.find_all(text=True), translations):
        elem.replace_with(translation)
    
    return str(soup)

# ✗ Bad - Lose formatting
def translate_html(html_text, target_lang):
    text = strip_tags(html_text)
    return translate(text, target_lang)
```

### 6. Set Appropriate TTLs

```javascript
// Content type based TTL
const TTL_MAP = {
  'ui.button': null,              // Never expire
  'quiz.title': 30 * 24 * 60 * 60, // 30 days
  'user.comment': 7 * 24 * 60 * 60, // 7 days
  'temp.preview': 60 * 60,         // 1 hour
};

function getCacheTTL(contentType) {
  return TTL_MAP[contentType] || 24 * 60 * 60; // Default 1 day
}
```

### 7. Implement Rate Limiting

```javascript
// Client-side rate limiting
class RateLimiter {
  constructor(maxRequests, windowMs) {
    this.maxRequests = maxRequests;
    this.windowMs = windowMs;
    this.requests = [];
  }
  
  async checkLimit() {
    const now = Date.now();
    // Remove old requests
    this.requests = this.requests.filter(
      time => now - time < this.windowMs
    );
    
    if (this.requests.length >= this.maxRequests) {
      const oldestRequest = Math.min(...this.requests);
      const waitTime = this.windowMs - (now - oldestRequest);
      throw new Error(`Rate limit exceeded. Wait ${waitTime}ms`);
    }
    
    this.requests.push(now);
  }
}
```

### 8. Pre-translate Common Content

```javascript
// Pre-translate frequently used phrases
const COMMON_PHRASES = [
  'Welcome',
  'Login',
  'Sign Up',
  'Submit',
  'Cancel',
  // ... more
];

async function preTranslateCommonPhrases() {
  const languages = ['es', 'fr', 'de', 'ja', 'zh'];
  
  for (const lang of languages) {
    const translations = await batchTranslate(COMMON_PHRASES, lang);
    
    // Cache with permanent TTL
    for (let i = 0; i < COMMON_PHRASES.length; i++) {
      await cache.set(
        COMMON_PHRASES[i],
        'en',
        lang,
        translations[i],
        null // Never expire
      );
    }
  }
}
```

---

## Appendix

### Language Codes Reference

Common ISO 639-1 language codes:

| Code | Language | Native Name |
|------|----------|-------------|
| en | English | English |
| es | Spanish | Español |
| fr | French | Français |
| de | German | Deutsch |
| it | Italian | Italiano |
| pt | Portuguese | Português |
| ru | Russian | Русский |
| zh | Chinese | 中文 |
| ja | Japanese | 日本語 |
| ko | Korean | 한국어 |
| ar | Arabic | العربية |
| hi | Hindi | हिन्दी |

### Cost Calculator

```javascript
// Estimate translation costs
function calculateCost(charCount, targetLangCount) {
  const costPerChar = 0.00002; // $20 per 1M characters
  const totalChars = charCount * targetLangCount;
  return totalChars * costPerChar;
}

// Example: Translate 1000 characters to 10 languages
const cost = calculateCost(1000, 10);
console.log(`Estimated cost: $${cost.toFixed(4)}`); // $0.0020
```

### Useful Links

- [Google Cloud Translation API Documentation](https://cloud.google.com/translate/docs)
- [Supported Languages](https://cloud.google.com/translate/docs/languages)
- [Pricing Calculator](https://cloud.google.com/products/calculator)
- [Best Practices Guide](https://cloud.google.com/translate/docs/best-practices)

---

**Document Version**: 1.0  
**Last Updated**: November 12, 2025

(() => {
  const { measurementId, siteUrl } = document.currentScript.dataset;
  const site = new URL(siteUrl);
  if (location.origin !== site.origin || !location.pathname.startsWith(site.pathname)
      || document.querySelector('meta[name="robots"]')?.content.includes('noindex')) return;

  const settings = document.querySelector('#analytics-settings');
  const notice = document.querySelector('#analytics-notice');
  const accept = notice.querySelector('[data-analytics-accept]');
  const decline = notice.querySelector('[data-analytics-decline]');
  const preferenceKey = 'portfolio-analytics-choice';
  const cookieLifetime = 180 * 24 * 60 * 60;
  const cookiePrefix = 'portfolio';
  const disableKey = `ga-disable-${measurementId}`;
  let allowed = false;
  let tagLoaded = false;
  let visitedSettings = false;

  const readChoice = () => {
    try {
      const choice = JSON.parse(localStorage.getItem(preferenceKey));
      return choice?.expires > Date.now() ? choice.allowed : null;
    } catch {
      return null;
    }
  };

  const loadTag = () => {
    if (tagLoaded) return;
    tagLoaded = true;
    const page = new URL(location.pathname, site);
    const campaign = new URLSearchParams(location.search);
    for (const field of ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term']) {
      const value = campaign.get(field);
      if (/^[a-z0-9_-]{1,80}$/i.test(value || '')) page.searchParams.set(field, value);
    }
    let referrer = '';
    if (document.referrer) referrer = new URL(document.referrer).origin;

    window.dataLayer ||= [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    const denied = { ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied' };
    window.gtag('consent', 'default', {...denied, analytics_storage: 'denied'});
    window.gtag('consent', 'update', { analytics_storage: 'granted' });
    window.gtag('js', new Date());
    window.gtag('config', measurementId, {
      page_location: page.href,
      page_referrer: referrer,
      cookie_domain: 'none',
      cookie_prefix: cookiePrefix,
      cookie_path: site.pathname,
      cookie_expires: cookieLifetime,
      cookie_update: false,
      allow_google_signals: false,
      allow_ad_personalization_signals: false,
    });

    const script = document.createElement('script');
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${measurementId}`;
    document.head.append(script);
  };

  const applyChoice = choice => {
    allowed = choice === true;
    window[disableKey] = !allowed;
    notice.hidden = choice !== null;
    settings.setAttribute('aria-expanded', String(!notice.hidden));
    if (allowed) loadTag();
    else {
      for (const cookie of document.cookie.split(';')) {
        const name = cookie.split('=')[0].trim();
        if (name.startsWith(`${cookiePrefix}_ga`)) {
          document.cookie = `${name}=; Max-Age=0; Path=${site.pathname}; Secure; SameSite=Lax`;
        }
      }
    }
  };

  const choose = choice => {
    try {
      localStorage.setItem(preferenceKey, JSON.stringify({ allowed: choice, expires: Date.now() + cookieLifetime * 1000 }));
    } catch {}
    applyChoice(choice);
    if (visitedSettings) settings.focus();
  };

  settings.hidden = false;
  settings.addEventListener('click', () => {
    visitedSettings = true;
    notice.hidden = false;
    settings.setAttribute('aria-expanded', 'true');
    notice.focus();
  });
  notice.addEventListener('keydown', event => {
    if (event.key === 'Escape' && visitedSettings) {
      notice.hidden = true;
      settings.setAttribute('aria-expanded', 'false');
      settings.focus();
    }
  });
  accept.addEventListener('click', () => choose(true));
  decline.addEventListener('click', () => choose(false));
  window.addEventListener('storage', event => {
    if (event.key === preferenceKey || event.key === null) applyChoice(readChoice());
  });
  applyChoice(readChoice());

  window.recordPortfolioEvent = (name, parameters) => {
    if (!allowed) return false;
    window.gtag('event', name, parameters || {});
    return true;
  };

  document.addEventListener('click', event => {
    const anchor = event.target.closest('a[href]');
    if (!anchor) return;
    if (anchor.protocol === 'mailto:') window.recordPortfolioEvent('email_click');
    else if (anchor.origin === site.origin && anchor.pathname === `${site.pathname}contact.html`) {
      const isQuote = new URL(anchor.href).searchParams.get('service') === 'brief';
      window.recordPortfolioEvent(isQuote ? 'quote_request_click' : 'contact_click');
    }
  });
})();

(function(){
  const key = 'jc-theme';
  const root = document.documentElement;
  const saved = localStorage.getItem(key);
  if(saved){ root.setAttribute('data-theme', saved); }
  document.addEventListener('DOMContentLoaded', function(){
    const btn = document.getElementById('themeToggle');
    if(!btn) return;
    btn.addEventListener('click', function(){
      const current = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      if(current === 'light') root.removeAttribute('data-theme'); else root.setAttribute('data-theme','dark');
      localStorage.setItem(key, current);
    });
  });
})();



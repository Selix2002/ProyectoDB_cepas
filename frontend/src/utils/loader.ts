// src/utils/loader.ts
import  loaderGif  from '../assets/img/loader.gif';
export function loader(show: boolean, gifUrl = loaderGif): void {
  const ID = 'global-loader';
  console.log('[loader] called with', { show, gifUrl });

  let el = document.getElementById(ID);
  console.log('[loader] existing element:', el);

  if (!el) {
    console.log('[loader] creating loader element');
    el = document.createElement('div');
    el.id = ID;
    Object.assign(el.style, {
      position: 'fixed',
      top: '0',
      left: '0',
      width: '100vw',
      height: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      backgroundColor: 'rgba(0, 0, 0, 0.5)',
      zIndex: '9999',
    });

    const img = document.createElement('img');
    console.log('[loader] setting img.src to', gifUrl);
    img.src = gifUrl;
    img.alt = 'Cargando...';
    Object.assign(img.style, {
      width: '80px',
      height: '80px',
    });

    img.onerror = (e) => {
      console.error('[loader] error loading gif:', e);
    };
    img.onload = () => {
      console.log('[loader] gif loaded successfully');
    };

    el.appendChild(img);
    document.body.appendChild(el);
    console.log('[loader] appended loader to body:', el);
  } else {
    console.log('[loader] element already exists, children:', el.children);
  }

  el.style.display = show ? 'flex' : 'none';
  console.log('[loader] set display to', el.style.display);
}

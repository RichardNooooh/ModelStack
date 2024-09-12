import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.tsx';
// import './index.css';
import { Auth0Provider } from '@auth0/auth0-react';

const authConfig = {
    domain: import.meta.env.VITE_AUTH0_DOMAIN,
    clientId: import.meta.env.VITE_AUTH0_CLIENTID,
    authorizationParams: {
        redirect_uri: window.location.origin,
    },
};

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Auth0Provider {...authConfig}>
      <App />
    </Auth0Provider>
  </StrictMode>,
)

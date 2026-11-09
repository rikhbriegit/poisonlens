/** @type {import('next').NextConfig} */
const nextConfig = {
  // Not a static export: the live audit runs server-side so the Ollama API key
  // never reaches the browser.
  images: { unoptimized: true },
};
export default nextConfig;

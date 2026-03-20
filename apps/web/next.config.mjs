/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
  transpilePackages: ["@cadris/schemas", "@cadris/client-sdk"],
  serverExternalPackages: ["unstorage", "unstorage/drivers/fs-lite"],
  eslint: {
    ignoreDuringBuilds: true
  }
};

export default nextConfig;

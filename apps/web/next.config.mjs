/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
  transpilePackages: ["@cadris/schemas", "@cadris/client-sdk"],
  eslint: {
    ignoreDuringBuilds: false
  }
};

export default nextConfig;

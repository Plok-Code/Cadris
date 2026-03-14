import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  transpilePackages: ["@cadris/schemas", "@cadris/client-sdk"],
  eslint: {
    ignoreDuringBuilds: true
  }
};

export default nextConfig;

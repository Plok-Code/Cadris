import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  transpilePackages: ["@cadris/schemas", "@cadris/client-sdk"],
  eslint: {
    ignoreDuringBuilds: true
  }
};

export default nextConfig;

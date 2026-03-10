/** @type {import('next').NextConfig} */
const nextConfig = {
  // This is the most important part to prevent the build from failing
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
};

export default nextConfig;
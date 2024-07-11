// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

// Removed dotenv require and config as it's causing module not found error
// const dotenv = require('dotenv');
// dotenv.config({ path: '../.env' });

const GTAG_DOC = process.env.GTAG_DOC;
const GTMAN_DOC = process.env.GTMAN_DOC;

import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'SalesGPT Docs',
  tagline: 'Get up to speed with SalesGPT',
  favicon: '/img/sgpt_fav.ico',

  // Set the production url of your site here
  url: 'https://your-docusaurus-site.example.com',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'filip-michalsky', // Usually your GitHub org/user name.
  projectName: 'SalesGPT', // Usually your repo name.

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          routeBasePath: '/', 
          sidebarPath: './sidebars.js',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/filip-michalsky/salesgpt/tree/main/', //the main is the branch name specified 
        },
        blog: false, 
        //blog: {
        //  showReadingTime: true,
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          //editUrl:
            //'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
        //},
        theme: {
          customCss: './src/css/custom.css',
        },
        gtag: {
          trackingID: GTAG_DOC,
          anonymizeIP: true,
        },
        googleTagManager: {
            containerId: GTMAN_DOC,
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/robot_mascot.ico',
      navbar: {
        title: 'SalesGPT',
        logo: {
          alt: 'My Site Logo',
          src: 'img/robot_mascot.ico',
        },
        
        items: [
        {
          to: '/Use_Cases/Mattress_salesman',
          position: 'left',
          label: 'Use Cases',
        },
        
          {href: 'https://salesgpt-api.vercel.app', label: 'API', position: 'left'},
          {
            href: 'https://github.com/filip-michalsky/salesgpt',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Docs',
            items: [
              {
                label: 'Tutorial',
                to: '/',
              },
            ],
          },
          /*
          {
            title: 'Community',
            items: [
              {
                label: 'Stack Overflow',
                href: 'https://stackoverflow.com/questions/tagged/docusaurus',
              },
              {
                label: 'Discord',
                href: 'https://discordapp.com/invite/docusaurus',
              },
              {
                label: 'Twitter',
                href: 'https://twitter.com/docusaurus',
              },
            ],
          }, 
          {
            title: 'More',
            items: [
              {
                label: 'Blog',
                to: '/blog',
              },
              {
                label: 'GitHub',
                href: 'https://github.com/facebook/docusaurus',
              },
            ],
          },*/
        ],
        copyright: `Copyright © ${new Date().getFullYear()} SalesGPT, Filip Michalsky & Honza Michna`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;


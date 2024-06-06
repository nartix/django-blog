import { defineConfig } from 'vite';
import dns from 'dns';
import path from 'path';
import fs from 'fs';

dns.setDefaultResultOrder('verbatim');

function getHtmlEntries(startPath) {
  let entries = {};

  // Check if directory exists
  if (!fs.existsSync(startPath)) {
    console.error(`Directory ${startPath} does not exist.`);
    return entries;
  }

  // Read all files in the directory
  const files = fs.readdirSync(startPath);

  files.forEach((file) => {
    const fullPath = path.join(startPath, file);

    if (fs.statSync(fullPath).isDirectory()) {
      // If it's a directory, recursively get entries
      const subEntries = getHtmlEntries(fullPath);
      entries = { ...entries, ...subEntries };
    } else if (file.endsWith('.html')) {
      // If it's an HTML file, add it to the entries
      const name = path.basename(file, '.html');
      entries[name] = fullPath;
    }
  });

  return entries;
}

export default defineConfig({
  server: {
    port: 3000,
    host: true, // or '0.0.0.0'
  },
  // build: {
  //   rollupOptions: {
  //     input: {
  //       ...getHtmlEntries(path.resolve(__dirname, 'components')),
  //       index: path.resolve(__dirname, 'index.html'), // Include the index.html file at the root directory
  //     },
  //   },
  // },
});

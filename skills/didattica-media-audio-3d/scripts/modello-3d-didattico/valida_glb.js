#!/usr/bin/env node
/* Valida un file GLB con il validatore ufficiale Khronos (gltf-validator).
   Uso:  node valida_glb.js file.glb
   Richiede:  npm install gltf-validator   (nella cartella di lavoro)
   Esito: stampa errori/avvisi/info; exit code 1 se ci sono errori. */
const { readFileSync } = require("fs");
const path = require("path");
const { createRequire } = require("module");

let validator;
try {
  validator = require("gltf-validator");            // node_modules accanto allo script
} catch (e) {
  const req = createRequire(path.join(process.cwd(), "package.json"));
  validator = req("gltf-validator");                // node_modules della cartella di lavoro
}

const file = process.argv[2] || "linea_del_tempo_3d.glb";
validator.validateBytes(new Uint8Array(readFileSync(file)))
  .then((report) => {
    const issues = report.issues;
    console.log(JSON.stringify({
      uri: file,
      errors: issues.numErrors,
      warnings: issues.numWarnings,
      infos: issues.numInfos,
      messages: issues.messages.filter(m => m.severity !== 0).slice(0, 10),
    }, null, 2));
    process.exit(issues.numErrors ? 1 : 0);
  })
  .catch((e) => { console.error(e); process.exit(1); });

const lib = Process.enumerateModules()[0];
const pattern = '64 75 63 74 66 7b';

function scanMemory(module, pattern) {
  Memory.scan(module.base, module.size, pattern, {
    onMatch(addr) {
      console.log("\n[*] Match!");
      console.log("[*] Addr: " + addr);
      console.log("[*] String: " + ptr(addr).readCString());
    },
    onError(reason) {
      console.log("[!] Error: " + reason);
    },
    onComplete() {
      console.log("[*] Complete!");
    },
  });
}

scanMemory(lib, pattern);

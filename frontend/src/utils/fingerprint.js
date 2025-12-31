import FingerprintJS from '@fingerprintjs/fingerprintjs';

let cachedFingerprint = null;

export const getFingerprint = async () => {
  if (cachedFingerprint) {
    return cachedFingerprint;
  }

  try {
    const fp = await FingerprintJS.load();
    const result = await fp.get();
    cachedFingerprint = result.visitorId;
    return cachedFingerprint;
  } catch (error) {
    console.error('Fingerprint error:', error);
    return 'fallback_' + Date.now();
  }
};
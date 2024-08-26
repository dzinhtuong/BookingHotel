import i18next from "i18next";
import { initReactI18next } from "react-i18next";
import translationVN from '../src/utils/switchLanguage/vn/translation.json';
import translationEN from '../src/utils/switchLanguage/en/translation.json';

i18next
    .use(initReactI18next)
    .init({
        debug: true,
        fallbackLng: 'vn',
        resources: {
            vn: {
                translation: translationVN
            },
            en: {
                translation: translationEN
            }
        }
    })
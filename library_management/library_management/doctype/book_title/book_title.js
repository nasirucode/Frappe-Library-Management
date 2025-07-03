// Copyright (c) 2025, Isyaku Murtala and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Book Title", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on('Book Title', {
    onload: function (frm) {
        frappe.call({
            method: "frappe.translate.get_all_languages",
            callback: function (r) {
                if (Array.isArray(r.message)) {
                    const standard_languages = {
                        "zh-TW": "Chinese (Traditional)",
                        "zh": "Chinese (Simplified)",
                        "vi": "Vietnamese",
                        "uz": "Uzbek",
                        "ur": "Urdu",
                        "uk": "Ukrainian",
                        "tr": "Turkish",
                        "th": "Thai",
                        "te": "Telugu",
                        "ta": "Tamil",
                        "sw": "Swahili",
                        "sv": "Swedish",
                        "sr-BA": "Serbian (Bosnia)",
                        "sr": "Serbian",
                        "sq": "Albanian",
                        "sl": "Slovenian",
                        "sk": "Slovak",
                        "si": "Sinhala",
                        "rw": "Kinyarwanda",
                        "ru": "Russian",
                        "ro": "Romanian",
                        "pt-BR": "Portuguese (Brazil)",
                        "pt": "Portuguese",
                        "ps": "Pashto",
                        "pl": "Polish",
                        "no": "Norwegian",
                        "nl": "Dutch",
                        "my": "Burmese",
                        "ms": "Malay",
                        "mr": "Marathi",
                        "mn": "Mongolian",
                        "ml": "Malayalam",
                        "mk": "Macedonian",
                        "lv": "Latvian",
                        "lt": "Lithuanian",
                        "lo": "Lao",
                        "ku": "Kurdish",
                        "ko": "Korean",
                        "kn": "Kannada",
                        "km": "Khmer",
                        "ja": "Japanese",
                        "it": "Italian",
                        "is": "Icelandic",
                        "id": "Indonesian",
                        "hu": "Hungarian",
                        "hr": "Croatian",
                        "hi": "Hindi",
                        "he": "Hebrew",
                        "gu": "Gujarati",
                        "fr-CA": "French (Canada)",
                        "fr": "French",
                        "fil": "Filipino",
                        "fi": "Finnish",
                        "fa": "Persian (Farsi)",
                        "et": "Estonian",
                        "es-PE": "Spanish (Peru)",
                        "es-NI": "Spanish (Nicaragua)",
                        "es-MX": "Spanish (Mexico)",
                        "es-GT": "Spanish (Guatemala)",
                        "es-EC": "Spanish (Ecuador)",
                        "es-DO": "Spanish (Dominican Republic)",
                        "es-CO": "Spanish (Colombia)",
                        "es-CL": "Spanish (Chile)",
                        "es-BO": "Spanish (Bolivia)",
                        "es-AR": "Spanish (Argentina)",
                        "es": "Spanish",
                        "eo": "Esperanto",
                        "en-US": "English (US)",
                        "en-GB": "English (UK)",
                        "en": "English",
                        "el": "Greek",
                        "de": "German",
                        "da-DK": "Danish (Denmark)",
                        "da": "Danish",
                        "cs": "Czech",
                        "ca": "Catalan",
                        "bs": "Bosnian",
                        "bo": "Tibetan",
                        "bn": "Bengali",
                        "bg": "Bulgarian",
                        "ar": "Arabic",
                        "am": "Amharic",
                        "af": "Afrikaans"
                    }


                    const language_options = r.message.map(code => ({
                        label: standard_languages[code] || code,
                        value: code
                    }));

                    language_options.sort((a, b) => a.label.localeCompare(b.label));

                    frm.set_df_property("language", "options", language_options);
                    frm.refresh_field("language");
                }
            }
        });
    }
});

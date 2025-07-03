// Copyright (c) 2025, Isyaku Murtala and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Book", {
// 	refresh(frm) {

// 	},
// });

// Trigger logic when the 'Book' form is loaded
frappe.ui.form.on('Book', {
    // When genre is selected or changed
    genre: function (frm) {
        // Dynamically filter sub_genre options based on selected genre
        frm.set_query('sub_genre', function () {
            return {
                filters: {
                    genre: frm.doc.genre
                }
            };
        });

        // Clear previously selected sub_genre (optional)
        frm.set_value('sub_genre', null);
    },
    onload: function (frm) {
        // Make a backend call to get the list of system languages
        frappe.call({
            method: "frappe.translate.get_all_languages",
            callback: function (r) {

                // Ensure the response is a valid array of language codes
                if (Array.isArray(r.message)) {

                    // Define a map of language codes to human-readable names
                    // These names are used as labels in the dropdown
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
                    };

                    // Convert the raw list of language codes into an array of
                    // { label, value } pairs to display in the dropdown
                    const language_options = r.message.map(code => {
                        return {
                            label: standard_languages[code] || code, // Use readable name if available, else fallback to code
                            value: code
                        };
                    });

                    // Optional: Sort the dropdown list alphabetically by label
                    language_options.sort((a, b) => a.label.localeCompare(b.label));

                    // Update the 'language' field's options dynamically
                    frm.set_df_property("language", "options", language_options);

                    // Refresh the field UI so the new options are shown immediately
                    frm.refresh_field("language");

                } else {
                    // Log a warning if the returned data is not an array
                    console.warn("Unexpected response for languages:", r.message);
                }
            }
        });
    },

});


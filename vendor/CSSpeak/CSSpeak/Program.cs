using Microsoft.Win32;
using System;
using System.Collections.Generic;
using System.Speech.Synthesis;
using System.Text;

namespace CSSpeak
{
    class Program
    {
        static void Main(string[] args)
        {
            string textToSpeak = "Say something.";
            if (args.Length == 1)
            {
                textToSpeak = args[0];
            }

            using (SpeechSynthesizer synth = new SpeechSynthesizer())
            {
                synth.SetOutputToNull();
                synth.PhonemeReached += new EventHandler<PhonemeReachedEventArgs>(synth_PhonemeReached);
                synth.Speak(textToSpeak);
            }
        }

        private static void synth_PhonemeReached(object sender, PhonemeReachedEventArgs e)
        {
            Console.Write(phoneConverter(e.Phoneme));
        }

        private static string phoneConverter(string input)
        {
            Dictionary<int, string> phoneMapping = new Dictionary<int, string>();
            RegistryKey rk = Registry.LocalMachine;
            RegistryKey sk = rk.OpenSubKey(@"SOFTWARE\Microsoft\Speech\PhoneConverters\Tokens\English");
            string[] stringArray = sk.GetValue("PhoneMap").ToString().Split(' ');
            for (int i = 0; i < stringArray.Length - 1; i += 2)
            {
                phoneMapping.Add(int.Parse(stringArray[i + 1], System.Globalization.NumberStyles.HexNumber), stringArray[i]);
            }

            StringBuilder sb = new StringBuilder();
            foreach (var c in input.ToCharArray())
            {
                sb.Append(phoneMapping[(int)c]);
            }

            sb.Append(" ");
            return sb.ToString();
        }
    }
}

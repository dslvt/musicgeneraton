c4=60
name_notes = ['c', 'd-', 'd', 'e-', 'e', 'f', 'g-', 'g', 'a-', 'a', 'b-', 'b']
scales = {'Adonai Malakh':                      '111101010110',
          'Aeolian Flat 1':                     '100110101101',
          'Algerian':                           '101101111001', 
          'Bi Yu':                              '100100010010', 
          'Blues':                              '100101110010', 
          'Blues Diminished':                   '110110110110',
          'Blues Modified':                     '101101110010',
          'Blues Pentacluster':                 '111100100000',
          'Blues Phrygian':                     '110101110010',
          'Blues With Leading Tone':            '100101110011',
          'Chad Gadyo':                         '101101010000',
          'Chaio':                              '101001001010',
          'Chromatic Bebop':                    '111011010111',
          'Chromatic Diatonic Dorian':          '111101011110',
          'Chromatic Dorian':                   '111001011100',
          'Chromatic Dorian Inverse':           '100111010011',
          'Chromatic Hypodorian':               '101110011100',
          'Chromatic Hypodorian Inverse':       '100111001110',
          'Chromatic Hypolydian':               '110010111001',
          'Chromatic Hypolydian Inverse':       '110011101001',
          'Chromatic Hypophrygian Inverse':     '111001110100',
          'Chromatic Lydian':                   '110011100101',
          'Chromatic Lydian Inverse':           '110100111001',
          'Chromatic Mixolydian':               '111001110010',
          'Chromatic Mixolydian Inverse ':      '101001110011',
          'Chromatic Permuted Diatonic Dorian': '111011011101',
          'Chromatic Phrygian':                 '100111001011',
          'Chromatic Phrygian Inverse':         '111010011100',
          'Diminished Scale':                   '101101101101',
          'Dominant Bebop':                     '101011010111',
          'Dorian':                             '101101010110',
          'Dorian Aeolian':                     '101101011110',
          'Dorian Flat 5':                      '101101100110',
          'Dorico Flamenco':                    '110011011010',
          'Eskimo Hexatonic 2':                 '101010101001',
          'Eskimo Tetratonic':                  '101010010000',
          'Full Minor':                         '101101011111',
          'Genus Chromaticum':                  '110111011101',
          'Genus Diatonicum Veterum Correctum': '101011110101',
          'Genus Primum':                       '101001010000',
          'Genus Primum Inverse':               '100001010010',
          'Genus Secundum':                     '100011010101',
          'Gnossiennes':                        '101100110110',
          'Half-Diminished Bebop':              '110101111001',
          'Han-kumoi':                          '101001011000',
          'Harmonic Major':                     '101011011001',
          'Harmonic Minor':                     '101101011001',
          'Harmonic Minor Inverse':             '110011010110',
          'Harmonic Neapolitan Minor':          '111101011001',
          'Hawaiian':                           '101100010101',
          'Hira-joshi':                         '101100011000',
          'Honchoshi Plagal Form':              '110101100010',
          'Houseini':                           '101111011110',
          'Houzam':                             '100111010101',
          'Hungarian Major':                    '100110110110',
          'Ionian Sharp 5':                     '101011001101',
          'Iwato':                              '110001100010',
          'Jazz Minor':                         '101101010101',
          'Jazz Minor Inverse':                 '110101010110',
          'Kiourdi':                            '101101111110',
          'Kokin-joshi, Miyakobushi':           '110001010010',
          'Kung':                               '101010100100',
          'Locrian':                            '110101101010',
          'Locrian 2':                          '101101101001',
          'Locrian Double-Flat 7':              '110101101100',
          'Locrian Natural 6':                  '110101100110',
          'Lydian':                             '101010110101',
          'Lydian Augmented':                   '101010101101',
          'Lydian Diminished':                  '101100110101',
          'Lydian Minor':                       '101010111010',
          'Lydian Sharp 2':                     '100110110101',
          'Magen Abot':                         '110110101101',
          'Major':                              '101011010101',
          'Major Bebop':                        '101011011101',
          'Major Gipsy':                        '110011011001',
          'Major Locrian':                      '101011101010',
          'Major Minor':                        '101011011010',
          'Major and Minor Mixed':              '101111011111',
          'Maqam Hijaz':                        '110011011011',
          'Maqam Shaddaraban':                  '110111100110',
          'Messiaen Mode 3':                    '111011101110',
          'Messiaen Mode 3 Inverse':            '101110111011',
          'Messiaen Mode 4':                    '111100111100',
          'Messiaen Mode 4 Inverse':            '100111100111',
          'Messiaen Mode 5':                    '111000111000',
          'Messiaen Mode 5 Inverse':            '100011100011',
          'Messiaen Mode 6':                    '111010111010',
          'Messiaen Mode 6 Inverse':            '101011101011',
          'Messiaen Mode 7':                    '111110111110',
          'Messiaen Mode 7 Inverse:':           '101111101111',
          'Messiaen Truncated Mode 2':          '110100110100',
          'Messiaen Truncated Mode 3':          '110011001100',
          'Messiaen Truncated Mode 3 Inverse':  '100110011001',
          'Messiaen Truncated Mode 5':          '110000110000',
          'Messiaen Truncated Mode 5 Inverse':  '100001100001',
          'Messiaen Truncated Mode 6':          '101000101000',
          'Messiaen Truncated Mode 6 Inverse':  '100010100010',
          'Minor':                              '101101011010',
          'Minor Bebop':                        '101111010110',
          'Minor Gipsy':                        '101100111001',
          'Minor Locrian':                      '101101101010', 
          'Minor Pentatonic With Leading Tones':'101111110111', 
          'Mixolydian':                         '101011010110', 
          'Mixolydian Flat 5':                  '101011100110',
          'Mixolydian Sharp 5':                 '101011001110',
          'Moorish Phrygian':                   '110111011011',
          'Neapolitan Major':                   '110101010101',
          'Neapolitan Minor':                   '110101011001',
          'Neapolitan Minor Mode':              '111010101100',
          'Neveseri':                           '110100111011',
          'Nohkan':                             '101001101101',
          'Oriental':                           '110011100110',
          'Oriental Pentacluster':              '111001100000',
          'Overtone':                           '101010110110',
          'Pelog':                              '110100011000',
          'Phrygian':                           '110101011010',
          'Phrygian Aeolian':                   '111101011010',
          'Phrygian Flat 4':                    '110110011010',
          'Phrygian Locrian':                   '110101111010',
          'Prokofiev Scale':                    '110101101011',
          'Prometheus':                         '101010100110',
          'Prometheus Neapolitan':              '110010100110',
          'Ritsu':                              '110101001010',
          'Rock n Roll':                        '100111010110',
          'Romanian Bacovia':                   '100011001001',
          'Romanian Major':                     '110010110110',
          'Sabach':                             '101110011010',
          'Sakura Pentatonic':                  '110001011000',
          'Sansagari':                          '100001000010',
          'Scriabin':                           '110010010100',
          'Shostakovich Scale':                 '110110110101',
          'Spanish Pentacluster':               '110111000000',
          'Spanish Phrygian':                   '110111011010',
          'Super Locrian':                      '110110101010',
          'Taishikicho, Ryo':                   '101011110111',
          'Takemitsu Tree Line Mode 1':         '101100101001',
          'Takemitsu Tree Line Mode 2':         '101100101010',
          'Twelve-Tone Chromatic':              '111111111111', 
          'Ultra Locrian':                      '110110101100',
          'Unison':                             '100000000000',
          'Ute Tritonic':                       '100100000010',
          'Utility Minor':                      '101101011011',
          'Verdi Enigmatic':                    '110011101011',
          'Verdi Enigmatic Ascending':          '110010101011',
          'Verdi Enigmatic Descending':         '110011001011',
          'Warao Tetratonic':                   '101100000010',
          'Wholetone Scale':                    '101010101010',
          'Wholetone Scale With Leading Tone':  '101010101011',
          'Youlan Scale':                       '111011110110',
          'Zirafkend':                          '101101011010'}


input_files = {
    "in/Star Trek TNG kurz.mid": "F minor", "in/sleepsat.mid": "E- major", "in/silentnight.mid": "C major",
    "in/shephard.mid": "F major", "in/sesame.mid": "C minor",
    "in/scooby.mid": "C major", "in/Sara.mid": "C major", "in/santacom.mid": "C major", "in/rudolph.mid": "C major",
    "in/Rikasmies.mid": "C minor",
    "in/reichwaehr.mid": "C minor", "in/prima.mid": "C major", "in/policeacademy.mid": "C major",
    "in/pipi-langstrumpf.mid": "C major", "in/Petteri.mid": "C major",
    "in/superman.mid": "G major", "in/StheB.mid": "G major", "in/Sternenhimmel.mid": "G major",
    "in/starwars-imperial.mid": "D minor", "in/starwars.mid": "C minor",
    "in/99 Luftballons.mid": "D minor", "in/90210.mid": "F major", "in/Zorbas.mid": "D major",
    "in/ZieGindsKomtDeStoomboot.mid": "F major",
    "in/you R not alone.mid": "D minor",
    "in/X Files.mid": "E minor", "in/winnerabba.mid": "B major", "in/WalkOfLife.mid": "A major",
    "in/Uralinpihlaja.mid": "D minor", "in/tlc.mid": "C major",
    "in/Titanic.mid": "C major", "in/tannebaum.mid": "F major",

    "in/oxygen.mid": "C minor", "in/ohcome.mid": "D minor", "in/Oh_come.mid": "G major",
    "in/offspring_getajob.mid": "A minor", "in/o_little.mid": "F major",
    "in/o_la_paloma.mid": "G major", "in/nur getrumt.mid": "C major",
    "in/Niemals in New York 2.mid": "C major", "in/nie wieder.mid": "C major", "in/murka.mid": "D minor",
    "in/Mit 66 Jahren.mid": "F major", "in/Mission_impossible.mid": "E- major",
    "in/mief.mid": "C major", "in/marmor-stein.mid": "C major",
    "in/major tom.mid": "F major", "in/Macarena.mid": "F major",
    "in/LivingRoom.mid": "D minor", "in/liquido.mid": "A minor",

    "in/Lindenstrae2.mid": "C major", "in/kiss.mid": "A minor", "in/Insel m. 2 Bergen.mid": "C major",
    "in/indiana.mid": "C major", "in/howmuchisthefish.mid": "A minor", "in/HoheBerge.mid": "D major",
    "in/GWein.mid": "A minor",

    "in/GuteZeiten.mid": "A minor", "in/Griechischer Wein2.mid": "A minor",
    "in/goodbad.mid": "A minor", "in/good.mid": "F major", "in/godfather.mid": "C minor",
    "in/god_rest.mid": "D minor", "in/gl_ck.mid": "C major", "in/FofS.mid": "G major",

    "in/flintstones.mid": "A minor", "in/flieger.mid": "C major",
    "in/Eldanka.mid": "D minor", "in/Elamaa_juoksuhaudoissa.mid": "G minor",
    "in/einfallfuer2.mid": "A minor", "in/Ein_Fall_Fuer_Zwei.mid": "A minor",
    "in/east_end.mid": "B- major", "in/DschingesKhan.mid": "A minor",
    "in/deutschlandlied.mid": "G major", "in/denneboom.mid": "F major",
    # "in/davy.mid": "C major",
    "in/Cucaracha.mid": "C major",
    "in/cccp.mid": "A major", "in/boom.mid": "F major", "in/Bittersweetharmonie.mid": "A- major",
    "in/big big girl.mid": "C major", "in/Biene Maja.mid": "C major",
    "in/away.mid": "F major", "in/advkal8.mid": "C major", "in/advkal10.mid": "C major",
    "in/advkal12.mid": "A minor", "in/advkal15.mid": "C major",
    "in/advkal17.mid": "C major"

}


midis = ["slow dancing.mid", "random.mid", "ramen king.mid", "Ocarina of Time.mid", "new_song.mid", "mozart.mid", "major-scale.mid", 
        "giselle.mid", "garbadje.mid", "check.mid", "amazing grace.mid"]
import random

# Jeffrey Adgate "Jeff" Dean (born July 23, 1968) is an American computer
# scientist and software engineer known for working at Google.

# pylint: disable=line-too-long
JEFF_DEAN_FACTS = [
    "1. During his own Google interview, Jeff Dean was asked the implications if P=NP were true. He said, 'P = 0 or N = 1'. Then, before the interviewer had even finished laughing, Jeff examined Google's public certificate and wrote the private key on the whiteboard.",
    "2. Compilers don't warn Jeff Dean. Jeff Dean warns compilers.",
    "3. The rate at which Jeff Dean produces code jumped by a factor of 40 in late 2000 when he upgraded his keyboard to USB 2.0.",
    "4. Jeff Dean builds his code before committing it, but only to check for compiler and linker bugs.",
    "5. When Jeff Dean has an ergonomic evaluation, it is for the protection of his keyboard.",
    "6. gcc -O4 emails your code to Jeff Dean for a rewrite.",
    "7. Jeff Dean once failed a Turing test when he correctly identified the 203rd Fibonacci number in less than a second.",
    "8. The speed of light in a vacuum used to be about 35 mph. Then Jeff Dean spent a weekend optimizing physics.",
    "9. Jeff Dean was born on December 31, 1969 at 11:48 PM. It took him twelve minutes to implement his first time counter.",
    "10. Jeff Dean eschews both Emacs and VI. He types his code into zcat, because it's faster that way.",
    "11. When Jeff Dean sends an ethernet frame there are no collisions because the competing frames retreat back up into the buffer memory on their source nic.",
    "12. Unsatisfied with constant time, Jeff Dean created the world's first O(1/N) algorithm.",
    "13. When Jeff Dean goes on vacation, production services across Google mysteriously stop working within a few days.",
    "14. Jeff Dean was forced to invent asynchronous APIs one day when he optimized a function so that it returned before it was invoked.",
    "15. When Jeff Dean designs software, he first codes the binary and then writes the source as documentation.",
    "16. Jeff Dean wrote an O(N2) algorithm once. It was for the Traveling Salesman Problem.",
    "17. Jeff Dean once implemented a web server in a single printf() call. Other engineers added thousands of lines of explanatory comments but still don't understand exactly how it works. Today that program is the front-end to Google Search.",
    "18. Jeff once simultaneously reduced all binary sizes by 3% and raised the severity of a previously known low-priority python bug to critical-priority in a single change that contained no python code.",
    "19. Jeff Dean can beat you at connect four. In three moves.",
    "20. When your code has undefined behavior, you get a seg fault and corrupted data. When Jeff Dean's code has undefined behavior, a unicorn rides in on a rainbow and gives everybody free ice cream.",
    "21. When Jeff Dean fires up the profiler, loops unroll themselves in fear.",
    "22. Jeff Dean is still waiting for mathematicians to discover the joke he hid in the digits of PI.",
    "23. Jeff Dean's keyboard has two keys: 1 and 0.",
    "24. When Jeff has trouble sleeping, he Mapreduces sheep.",
    "25. When Jeff Dean listens to mp3s, he just cats them to /dev/dsp and does the decoding in his head.",
    "26. When Graham Bell invented the telephone, he saw a missed call from Jeff Dean.",
    "27. Jeff Dean's watch displays seconds since January 1st, 1970. He is never late.",
    "28. Jeff starts his programming sessions with cat > /dev/mem.",
    "29. One day Jeff Dean grabbed his Etch-a-Sketch instead of his laptop on his way out the door. On his way back home to get his real laptop, he programmed the Etch-a-Sketch to play Tetris.",
    "30. Google search went down for a few hours in 2002, and Jeff Dean started handling queries by hand. Search Quality doubled.",
    "31. Jeff Dean puts his pants on one leg at a time, but if he had more legs, you would see that his approach is O(log(N)).",
    "32. The x86-64 spec includes several undocumented instructions marked private use. They are actually for Jeff Dean's use.",
    "33. Knuth mailed a copy of TAOCP to Google. Jeff Dean autographed it and mailed it back.",
    "34. When he heard that Jeff Dean's autobiography would be exclusive to the platform, Richard Stallman bought a Kindle.",
    "35. Jeff Dean once shifted a bit so hard, it ended up on another computer.",
    "36. Jeff Dean can losslessly compress random data.",
    "37. When asked if the facts about him are true, Jeff Dean responded '111111'. While the interviewer was still trying to figure out what he means, he clarified 'every single bit of it is true.'",
    "38. Jeff Dean mines bitcoins. In his head.",
    "39. Jeff Dean knows the last digit of Pi.",
]


def random_jeff_dean() -> str:
    return random.choice(JEFF_DEAN_FACTS)

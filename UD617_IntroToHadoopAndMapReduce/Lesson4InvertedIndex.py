__author__ = 'Marc'
#!/usr/bin/python
"""
A mapper function that creates an inverted index for all of the words that
can be found in the body of a forum post and node id they can be found in.

Do not parse the HTML. Just split the text on all whitespace as well as the
following characters: .,!?:;"()<>[]#$=-/
"""
import sys
import csv
import re


def mapper():
    reader = csv.reader(sys.stdin, delimiter='\t')
    writer = csv.writer(sys.stdout, delimiter='\t', quotechar='"', quoting=csv.QUOTE_ALL)

    iindex = {}
    for line in reader:
        id = line[0]
        body = line[4]
        words = re.split(' |\.|,|!|\?|:|;|"|\(|\)|<|>|\[|\]|#|\$|=|-|\/', body)
        for word in words:
            if word.lower() in iindex and id not in iindex[word.lower()]:
                iindex[word.lower()].append(id)
            else:
                iindex[word.lower()] = [id]


test_text = """"id"	"title"	"tagnames"	"author_id"	"body"	"node_type"	"parent_id"	"abs_parent_id"	"added_at"	"score"	"state_string"	"last_edited_id"	"last_activity_by_id"	"last_activity_at"	"active_revision_id"	"extra"	"extra_ref_id"	"extra_count"	"marked"
"5339"	"Whether pdf of Unit and Homework is available?"	"cs101 pdf"	"100000458"	""	"question"	"\N"	"\N"	"2012-02-25 08:09:06.787181+00"	"1"	""	"\N"	"100000921"	"2012-02-25 08:11:01.623548+00"	"6922"	"\N"	"\N"	"204"	"f"
"2312"	"Feedback on Audio Quality"	"cs101 production audio"	"100005361"	"<p>We are looking for feedback on the audio in our videos. Tell us what you think and try to be as <em>specific</em> as possible.</p>"	"question"	"\N"	"\N"	"2012-02-23 00:28:02.321344+00"	"2"	""	"\N"	"201398145"	"2014-01-14 17:18:35.613939+00"	"2960"	"\N"	"\N"	"524"	"f"
"2741"	"where is the sample page for homework?"	"cs101 missing_info homework"	"100001178"	"<p>I am sorry if I am being a nob ... but I do not seem to find any information regarding the sample page reffered to on the 1 question of homework 1.</p>
<p>Where can I get the sample page?</p>
<p>Cheers</p>"	"question"	"\N"	"\N"	"2012-02-23 09:15:02.270861+00"	"0"	"(closed)"	"10843"	"100001178"	"2012-02-23 10:36:43.165119+00"	"3513"	"\N"	"\N"	"169"	"t"
"6361"	"When will unit 2 be online?"	"cs101 unit2"	"100003292"	"<p>When will unit 2 be online?</p>"	"question"	"\N"	"\N"	"2012-02-26 15:47:12.522262+00"	"0"	"(closed)"	"51919"	"100003292"	"2012-03-03 10:12:27.41521+00"	"21196"	"\N"	"\N"	"186"	"t"
"7185"	"Hungarian group"	"cs101 hungarian nationalities"	"100003268"	"<p>Hi there!</p>
<p>Any Hungarians doing the course? We could form a group!<br>
;)</p>"	"question"	"\N"	"\N"	"2012-02-27 15:09:11.184434+00"	"0"	""	"\N"	"100003268"	"2012-02-27 15:09:11.184434+00"	"9322"	"\N"	"\N"	"106"	"f"
"26454"	"Course Application."	"cs101 application."	"100003192"	"<p>fantastic Please tell about the Course Application. How to use the Course for higher education and jobs?</p>"	"question"	"\N"	"\N"	"2012-03-08 08:34:06.704674+00"	"-1"	""	"\N"	"100003192"	"2012-03-08 08:34:06.704674+00"	"34477"	"\N"	"\N"	"73"	"f"
"3778"	"What profile information is public?"	"cs101 profile"	"100008254"	"<p>Is there a way to change what is and isn't publicly displayed?</p>"	"question"	"\N"	"\N"	"2012-02-23 22:00:39.134386+00"	"0"	"(closed)"	"90176"	"100002517"	"2012-03-08 22:12:34.271971+00"	"4876"	"\N"	"\N"	"228"	"t"
"262"	"Course content Opera browser error"	"cs101 browsers issues"	"100000425"	"<p>It wont work with the opera browser, guys. </p>"	"question"	"\N"	"\N"	"2012-02-21 10:57:22.321732+00"	"1"	""	"\N"	"100006616"	"2012-03-22 16:12:10.024851+00"	"332"	"\N"	"\N"	"393"	"f"
"15084"	"Digital Board used"	"cs101 withe board digital"	"100002999"	"<p>Hi Guys, </p>
<p>Does anyone know the model of the Digital Board the professor has been used during the course ?</p>
<p>I am also a online professor in Brazil and I am interested on that type of gadget.</p>
<p>Thanks, <br>
Augusto</p>"	"question"	"\N"	"\N"	"2012-03-02 13:35:40.964189+00"	"0"	""	"\N"	"100004557"	"2012-03-02 13:38:25.194134+00"	"19481"	"\N"	"\N"	"178"	"f"
"6336"	"Unit 1: Same Value Q"	"cs101 value same"	"100002404"	"<p>what is the difference between [S] and [s+s) ? are they the same </p>"	"question"	"\N"	"\N"	"2012-02-26 15:16:00.995176+00"	"0"	""	"\N"	"100003151"	"2012-02-26 15:55:45.238065+00"	"8249"	"\N"	"\N"	"151"	"f"
"3017"	"Homework #1"	"cs101 homework"	"100000972"	"<p>I didn't exactly understand what the 1st homework assignment question is about? Do we have to select options which are related to learning search engine or what?</p>"	"question"	"\N"	"\N"	"2012-02-23 12:39:58.31747+00"	"1"	""	"\N"	"100005361"	"2012-02-25 04:59:11.157605+00"	"3884"	"\N"	"\N"	"786"	"f"
"8002818"	""	"cs387 "	"100071233"	"<p>this is a little off this topic, but since 10^1 has two digits (10^2 three, 10^3 four etc.), wouldn't the numbers with 100 digits be {10^99, 10^99 + 1, ..., 10^100 - 1} ?</p>
<p>in that case, the answer would be 114 (with 227.95 rounded to 228).</p>
<p>could anyone please point out why they use 10^100 for a ""100-decimal-digit number"", when it has 101 digits?</p>"	"answer"	"8002110"	"8002110"	"2012-05-09 02:41:40.721625+00"	"0"	""	"\N"	"100008880"	"2012-09-30 01:46:20.565857+00"	"8004204"	"\N"	"\N"	"0"	"f"
"8002165"	""	"cs387 "	"100063037"	"<p>It states , that the complexity increases exponentially with the size of x. Assume x is a n-bit number. If x is close to $% 2^n - 1 $% , we approximately need to check those $% 2^n $% numbers. Now let y be a n+m-bit prime, assuming the highest bit is not zero. We now increased the pool of numbers to check from $% 2^n $% to $%2^m \cdot 2^n$%, so by increasing the number of bits by m we get in the worst case $% 2^m $% more modulo operations. Thats the trick ;)</p>
<p>Well these are only approximate arguments but i think the idea is clear.</p>"	"answer"	"8002157"	"8002157"	"2012-04-30 18:01:05.800986+00"	"2"	""	"8026669"	"100063037"	"2012-04-30 18:03:19.983628+00"	"8002945"	"\N"	"\N"	"0"	"f"
"""

# This function allows you to test the mapper with the provided test string
def main():
    import StringIO
    sys.stdin = StringIO.StringIO(test_text)
    mapper()
    sys.stdin = sys.__stdin__

main()
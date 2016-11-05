# textform
Python module to format values with a template string
like Perl format (perlform(1)).

In the template:

 @<<<<   Left justified field.
 @>>>>   Right justified field.
 @||||   Centered field.

Any other text in the template is copied through to the result.

The "~~" feature of Perl format is implied: repeat until all fields
are exhausted.

Example:

 textform.format("@<<<<<<<<:@|||||||:@>>>>>>>",
                 ["now is the time for all",
                  "good men to come",
                  "to the aid of their party"])

returns:

 "now is   :good men:  to the\n" +
 "the time :to come :  aid of\n" +
 "for all  :        :   their\n" +
 "         :        :   party"

This is a tool to facilitate the porting from cocos2d to cocos2d-x.

cocos2d is written in Objective-C language while cocos2d-x is written in C++
language.

Fortunately they both share a similar API. Therefore we can do basically one to
one mapping during the porting.

However, things are not that easy, if the project in cocos2d uses too much
Objective-C runtime features, the porting could be hairy.

This project uses plain text substitution method, no inner knowledge of
Objective-C is utilized. The next step for this project could be to parse the
Objective-C code into AST and then do a better source-to-source translation.

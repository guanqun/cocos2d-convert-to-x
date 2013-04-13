import re

lines = open('input.txt').readlines()
output_lines = []

direct_mapping = [ (r'BOOL',                r'bool'),
                   (r'TRUE',                r'true'),
                   (r'FALSE',               r'false'),
                   (r'import',              r'include'),
                   (r'CGRect',              r'CCRect'),
                   (r'CGSize',              r'CCSize'),
                   (r'CGPoint',             r'CCPoint'),
                   (r'CGFloat',             r'float'),
                   (r'UITouch',             r'CCTouch'),
                   (r'UIEvent',             r'CCEvent'),
                   (r'NSSet',               r'CCSet'),
                   (r'NSArray',             r'CCArray'),
                   (r'.contentSize',        r'->getContentSize()'),
                   (r'.boundingBox',        r'->boundingBox()'),
                   (r'%@',                  r'%s'),
                   (r'@',                   r''),
                   (r'NSLog',               r'CCLog'),
                   (r'.position.x',         r'->getPositionX()'),
                   (r'.position.y',         r'->getPositionY()'),
                   (r'nil',                 r'NULL'),
                   (r'NSMutableArray',      r'CCArray'),
                   (r'NSMutableDictionary', r'CCDictionary'),
                   (r'NSString',            r'CCString')
                 ]

properties = [ 'position',
               'scale',
               'opacity',
               'color',
               'contentSize',
               'tag',
               'zOrder'
             ]

actions = [ 'removeFromParentAndCleanup',
            'removeAllChildrenWithCleanup',
            'addChild',
            'removeObjectAtIndex',
            'addObject',
            'runAction'
          ]

for i in range(len(lines)):
    one_line = lines[i]

    # calculate the leading spaces
    ls = ''
    for j in one_line:
        if j == ' ' or j == '\t':
            ls += j
        else:
            break

    # addChild
    ss = re.split(r'\W+', one_line)
    ss = [x for x in ss if len(x) != 0]
    for j in actions:
        if len(ss) == 3 and ss[1] == j:
            one_line = ls + ss[0] + '->' + ss[1] + '(' + ss[2] + ');\n'

    # property settings: change   sprite.position = ccp(0, 0); to sprite->setPosition(ccp(0, 0));
    # property change should be modified before the direct mapping
    for j in properties:
        sp = '.' + j + ' = '
        ss = re.split(sp, one_line)
        if len(ss) == 2:
            ss[1] = re.sub(';', ');', ss[1])
            one_line = ss[0] + '->set' + j.capitalize() + '(' + ss[1]
            break

    # direct mapping
    for dm in direct_mapping:
        one_line = re.sub(dm[0], dm[1], one_line)

    # the order matters e.g. .position.x vs .position
    for j in properties:
        sp = '.' + j
        spnew = '->get' + j.capitalize() + '()'
        one_line = re.sub(sp, spnew, one_line)

    ss = re.split(' = ', one_line)
    if len(ss) == 2:
        sss = re.split('objectAtIndex:', ss[1])
        if len(sss) == 2:
            one_line = ss[0] + ' = ' + re.sub('\[', '', sss[0]) + '->objectAtIndex('  + re.sub(';', ');', re.sub('\]', '', sss[1]))

    output_lines.append(one_line)

# write back to this file
f = open('output.txt', 'w')
f.writelines(output_lines)
f.close()

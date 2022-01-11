#   --- imports ---
import random
from discord.ext.commands.core import check
import bot
from discord.ext import commands


#   --- setup ---

bot = commands.Bot(command_prefix = '>')
bot.remove_command('help')

file = open('words.txt', 'r')
list_of_words = []
for line in file:
    list_of_words.append(line.strip())
    
@bot.event
async def on_ready():
    print('rdy')
    

#   --- hangman ---

async def update_keyword(keyword_hidden, keyword, msg):
    tmp_keyword_string = keyword_hidden
    for i in range (len(keyword)):
        if msg == keyword[i]:
            tmp_keyword_string[i] = keyword[i]
        else:
            tmp_keyword_string[i] = keyword_hidden[i]
    return ''.join(str(e) for e in tmp_keyword_string) + ' (' + str(len(keyword)) + ')'
            

async def update_graph(attempt):
    if attempt == 0:   
        return '''> > Galgenraten:
        > 
        > 
        > 
        > 
        > 
        > 
        > '''
    elif attempt == 1:
        return '''> > Galgenraten:
        > 
        > 
        > 
        > 
        > 
        >  /
        > '''
    elif attempt == 2:
        return '''> > Galgenraten:
        > 
        >      
        >      
        >      
        >       
        >  / \ 
        > '''           
    elif attempt == 3:
        return '''> > Galgenraten:
        > 
        >     | 
        >     | 
        >     | 
        >     |  
        >  /_\ 
        > ''' 
    elif attempt == 4:
        return '''> > Galgenraten:
        >       \_\_\_\_\_\_ 
        >     | 
        >     | 
        >     | 
        >     |  
        >  /_\ 
        > ''' 
    elif attempt == 5:
        return '''> > Galgenraten:
        >       \_\_\_\_\_\_ 
        >     |/          
        >     |           
        >     |           
        >     |           
        >  /_\ 
        > ''' 
    elif attempt == 6:
        return '''> > Galgenraten:
        >       \_\_\_\_\_\_ 
        >     |/           |
        >     |          
        >     |          
        >     |           
        >  /_\ 
        > '''         
    elif attempt == 7:
        return '''> > Galgenraten:
        >       \_\_\_\_\_\_ 
        >     |/           |
        >     |            O
        >     |          
        >     |           
        >  /_\ 
        > ''' 
    elif attempt == 8:
        return '''> > Galgenraten:
        >       \_\_\_\_\_\_ 
        >     |/           |
        >     |            O
        >     |             |
        >     |           
        >  /_\ 
        > ''' 
    elif attempt == 9:
        return '''> > Galgenraten:
        >       \_\_\_\_\_\_ 
        >     |/           |
        >     |            O
        >     |           /|
        >     |           
        >  /_\ 
        > ''' 
    elif attempt == 10:
        return '''> > Galgenraten:
        >       \_\_\_\_\_\_ 
        >     |/           |
        >     |            O
        >     |           /|\\
        >     |           
        >  /_\ 
        > ''' 
    elif attempt == 11:
        return '''> > Galgenraten:
        >       \_\_\_\_\_\_ 
        >     |/           |
        >     |            O
        >     |           /|\\
        >     |           / 
        >  /_\ 
        > ''' 
    elif attempt == 12:
        return '''> > Galgenraten:
        >       \_\_\_\_\_\_ 
        >     |/           |
        >     |            O
        >     |           /|\\
        >     |           / \\
        >  /_\ 
        > ''' 
    
async def check_game_state(keyword_hidden, keyword, attempt):
    if attempt < 12 and keyword == keyword_hidden:
        print('1')
        return True, False
    elif attempt >= 12 and keyword != keyword_hidden:
        print('2')
        return False, True
    else:
        print('3')
        return False, False

def check(m):
    return len(m.content) == 1

async def hangman(ctx):
    keyword_as_string = list_of_words[random.randint(0, len(list_of_words))].lower()
    keyword = list(keyword_as_string)
    keyword_hidden = []
    for i in range (len(keyword)):
        keyword_hidden.append('\_')       
    attempt = 0
    used_letters = ['\n> ', 'Benutze Buchstaben: ']
    pic_str = await update_graph(attempt)   
    keyword_string = ''.join(str(e) for e in keyword_hidden) + f' ({str(len(keyword))})'
    await ctx.send(f'''
                   > > Regeln:    
                   >            - immer nur ein Buchstabe, auch wenn ihr das Wort schon kennt
                   >              es werden dabei keine extra Versuche gezählt
                   >            - nur Kleinbuchstaben
                   >            - keine Zahlen
                   >            - statt ö, ü, ä immer ae, ue, oe\n {pic_str} {keyword_string}''')
    for i in range (len(keyword_as_string) + 12):
        win, lose = await check_game_state(keyword_hidden, keyword, attempt)
        if win:
            message = f'> GG, mit {str(attempt)} Fehlversuchen gewonnen!'
            await ctx.send(message)
            break
        elif lose:
            message = f'> Nice try, leider nicht gut genug, das Wort war: {keyword_as_string}'
            await ctx.send(message)
            break
        else:  
            msg = await bot.wait_for('message', check=check)
            msg_str = msg.content.lower()
            if msg_str.isalpha():
                if msg_str in used_letters:
                    await ctx.send('> Der Buchstabe wurde schon benutzt.')
                else:  
                    if msg_str not in keyword:
                        attempt += 1        
                        pic_str = await update_graph(attempt)
                    elif msg_str in keyword:
                        pic_str = await update_graph(attempt)
                        keyword_string = await update_keyword(keyword_hidden, keyword, msg_str)
                    used_letters.append(msg_str)
                    used_letters_string = ''.join(str(e) for e in used_letters)
                    await ctx.send(pic_str + keyword_string + used_letters_string)
            else:
                await ctx.send('> Es kommen keine Ziffern oder Sonderzeichen vor.')
    
    
#   --- commands ---

@bot.command(pass_context = True, aliases = ['gr', 'galgenraten'])
async def hangman_(ctx):
    await hangman(ctx)   


#   --- events ---

@bot.event
async def on_message(message):  
    await bot.process_commands(message)

bot.run('YOUR_TOKEN')
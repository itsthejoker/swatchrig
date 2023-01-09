from utils import print_message

mainscreen = r"""
                         __         .__          .__        
  ________  _  _______ _/  |_  ____ |  |_________|__| ____  
 /  ___/\ \/ \/ /\__  \\   __\/ ___\|  |  \_  __ \  |/ ___\ 
 \___ \  \     /  / __ \|  | \  \___|   Y  \  | \/  / /_/  >
/____  >  \/\_/  (____  /__|  \___  >___|  /__|  |__\___  / 
     \/               \/          \/     \/        /_____/  
                                                            
       ╔════════════════╦════════╦════════╦════════╗        
       ║████████████████║▓▓▓▓▓▓▓▓║▒▒▒▒▒▒▒▒║░░░░░░░░║        
       ║██/\████████████║▓▓▓▓▓▓▓▓║▒▒▒▒▒▒▒▒║░░░░░░░░║        
       ║██\/████████████║▓▓▓▓▓▓▓▓║▒▒▒▒▒▒▒▒║░░░░░░░░║        
       ║████████████████║▓▓▓▓▓▓▓▓║▒▒▒▒▒▒▒▒║░░░░░░░░║        
       ╚════════════════╩════════╩════════╩════════╝        
                                                            
           │   press button  │     hold 3s      │           
           ├─────────────────┼──────────────────┼           
           │   take picture  │       sync       │           
                -- hold 10s for shutdown --                 
"""

print_message(mainscreen, initial_newlines=1, show_dude=False)

# Roll20 API Documentation

## Introduction

The Roll20 API (Application Programming Interface) is a powerful tool that allows Pro subscribers to enhance their games with custom JavaScript code. This guide provides an overview of the API's capabilities and how to use it effectively.

## Key Features

- Run custom JavaScript code in your Roll20 game
- Automate repetitive tasks
- Create custom commands and macros
- Enhance character sheets and game mechanics
- Integrate with external services (within sandbox limitations)
- Create and manage Mods for your game

## Roll20 Mods API

Roll20 Mods API is an extension of the Roll20 API that allows you to create modular, reusable scripts called Mods. Mods can be easily shared and installed in multiple games, making it easier to manage and distribute your custom functionality.

### Key Concepts

- **Mod**: A self-contained script package that can be installed and configured in a game.
- **Mod Authors**: Creators of Mods who can publish their work for others to use.
- **Mod Configuration**: Settings that can be adjusted by GMs without editing the code.
- **Mod Marketplace**: A platform for sharing and discovering Mods (coming soon).

### Creating a Mod

1. Write your script as usual in the API Scripts tab.
2. Use the `mod` object to define your Mod's properties and configuration options.
3. Implement the required Mod lifecycle methods.

Example:

```javascript
const myMod = {
    name: 'My Awesome Mod',
    version: '1.0',
    author: 'Your Name',
    config: {
        enableFeatureX: {
            type: 'checkbox',
            default: true,
            label: 'Enable Feature X'
        }
    },
    init: function() {
        // Initialization code
    },
    ready: function() {
        // Code to run when the game is ready
    },
    destroy: function() {
        // Cleanup code
    }
};

mod.register(myMod);
```

### Using Mods

- GMs can install Mods from the API Scripts tab.
- Mods can be configured without editing the code.
- Multiple versions of a Mod can be installed in the same game.

### Advanced Mod Features

#### State Management

Mods can use the `mod.state` object to store persistent data:

```javascript
const myMod = {
    // ... other properties ...
    ready: function() {
        if (!mod.state.hasOwnProperty('counter')) {
            mod.state.counter = 0;
        }
        log('Counter value: ' + mod.state.counter);
    }
};
```

#### Dependency Management

Mods can specify dependencies on other Mods:

```javascript
const myMod = {
    // ... other properties ...
    dependencies: ['OtherMod1', 'OtherMod2'],
    init: function() {
        // This will only run if OtherMod1 and OtherMod2 are installed and initialized
    }
};
```

#### Event Handling

Mods can use the standard Roll20 event system:

```javascript
const myMod = {
    // ... other properties ...
    ready: function() {
        on('chat:message', this.handleChatMessage);
    },
    handleChatMessage: function(msg) {
        if (msg.type === 'api' && msg.content.startsWith('!mymod')) {
            // Handle the command
        }
    }
};
```

#### Configuration UI

Mods can define a configuration UI for easy setup:

```javascript
const myMod = {
    // ... other properties ...
    config: {
        backgroundColor: {
            type: 'color',
            default: '#ffffff',
            label: 'Background Color'
        },
        fontSize: {
            type: 'number',
            default: 14,
            label: 'Font Size'
        }
    }
};
```

### Best Practices for Mod Development

1. **Modular Design**: Break your Mod into smaller, reusable functions.
2. **Error Handling**: Use try-catch blocks to prevent crashes.
3. **Performance**: Optimize for efficiency, especially in frequently called functions.
4. **Documentation**: Provide clear instructions for users and other developers.
5. **Versioning**: Use semantic versioning for your Mods.
6. **Testing**: Thoroughly test your Mod in various scenarios before publishing.

### Example: Dice Roller Mod

Here's a simple example of a Mod that adds a custom dice rolling command:

```javascript
const diceRollerMod = {
    name: 'Dice Roller',
    version: '1.0',
    author: 'Roll20 Developer',
    config: {
        defaultDice: {
            type: 'text',
            default: 'd20',
            label: 'Default Dice'
        }
    },
    ready: function() {
        on('chat:message', this.handleChatMessage);
    },
    handleChatMessage: function(msg) {
        if (msg.type === 'api' && msg.content.startsWith('!roll')) {
            const args = msg.content.split(' ');
            const dice = args[1] || mod.config.defaultDice;
            const result = randomInteger(parseInt(dice.replace('d', '')));
            sendChat('Dice Roller', `/w ${msg.who} You rolled a ${result} on ${dice}`);
        }
    }
};

mod.register(diceRollerMod);
```

This Mod adds a `!roll` command that users can use to roll dice, with a configurable default dice type.

## Getting Started

1. **Subscription**: You need a Pro subscription to access the API.
2. **API Scripts Tab**: Access it from the game's details page.
3. **Script Editor**: Write and edit your scripts here.
4. **API Console**: View script output and errors.
5. **Mod Management**: Install, configure, and manage Mods from the API Scripts tab.

## Basic Concepts

- **Events**: Scripts respond to game events (e.g., chat messages, token movements).
- **Objects**: Represent game elements (e.g., characters, handouts, tokens).
- **State**: Persistent storage for script data.
- **Sandbox**: Scripts run in a secure environment with limitations.
- **Mods**: Modular, reusable scripts that can be easily shared and configured.

## Writing Scripts

### Basic Structure

```javascript
on('ready', function() {
    log('Script loaded!');
});

on('chat:message', function(msg) {
    if(msg.content === '!hello') {
        sendChat('API', '/w ' + msg.who + ' Hello!');
    }
});
```

### Key Functions

- `on()`: Listen for events
- `log()`: Output to API Console
- `sendChat()`: Send messages to chat
- `createObj()`: Create game objects
- `getObj()`: Retrieve objects
- `findObjs()`: Search for objects

## Best Practices

1. **Efficiency**: Minimize API calls and use efficient queries.
2. **Error Handling**: Implement try-catch blocks for stability.
3. **Security**: Validate user input and respect permissions.
4. **Testing**: Thoroughly test in a development campaign before deployment.
5. **Documentation**: Comment your code and provide usage instructions.
6. **Modular Design**: Consider creating Mods for reusable functionality.
7. **Configuration Options**: Use Mod configurations to make your scripts more flexible.

## Limitations and Considerations

- No direct database access
- Limited external network access
- 5-second timeout for script execution
- 500ms cooldown between API commands
- Mods must follow specific structure and lifecycle methods

## Debugging

- Use `log()` for output to the API Console
- Enable Developer Mode in game settings for additional tools
- Check the API Sandbox console for errors
- Test Mods thoroughly in different game contexts

## Additional Mod Examples

### Basic Mod Examples

#### Hello World Mod

A simple Mod that responds to a chat command:

```javascript
const helloWorldMod = {
    name: 'Hello World',
    version: '1.0',
    author: 'Roll20',
    init: function() {
        on('chat:message', (msg) => {
            if (msg.type === 'api' && msg.content === '!hello') {
                sendChat('Hello World Mod', 'Hello, ' + msg.who + '!');
            }
        });
    }
};

mod.register(helloWorldMod);
```

#### Configurable Greeting Mod

A Mod with a configurable greeting:

```javascript
const greetingMod = {
    name: 'Configurable Greeting',
    version: '1.0',
    author: 'Roll20',
    config: {
        greeting: {
            type: 'text',
            default: 'Hello',
            label: 'Greeting Text'
        }
    },
    init: function() {
        on('chat:message', (msg) => {
            if (msg.type === 'api' && msg.content === '!greet') {
                sendChat('Greeting Mod', `${mod.config.greeting}, ${msg.who}!`);
            }
        });
    }
};

mod.register(greetingMod);
```

### Advanced Mod Examples

#### Token Mover Mod

A Mod that moves a token when a command is issued:

```javascript
const tokenMoverMod = {
    name: 'Token Mover',
    version: '1.0',
    author: 'Roll20',
    config: {
        distance: {
            type: 'number',
            default: 70,
            label: 'Movement Distance (px)'
        }
    },
    init: function() {
        on('chat:message', (msg) => {
            if (msg.type === 'api' && msg.content.startsWith('!move')) {
                const [, direction] = msg.content.split(' ');
                const token = getObj('graphic', msg.selected[0]._id);
                if (token) {
                    const distance = mod.config.distance;
                    switch (direction) {
                        case 'up':
                            token.set('top', token.get('top') - distance);
                            break;
                        case 'down':
                            token.set('top', token.get('top') + distance);
                            break;
                        case 'left':
                            token.set('left', token.get('left') - distance);
                            break;
                        case 'right':
                            token.set('left', token.get('left') + distance);
                            break;
                    }
                }
            }
        });
    }
};

mod.register(tokenMoverMod);
```

#### Initiative Tracker Mod

A more complex Mod that manages an initiative tracker:

```javascript
const initiativeTrackerMod = {
    name: 'Initiative Tracker',
    version: '1.0',
    author: 'Roll20',
    config: {
        announceRounds: {
            type: 'checkbox',
            default: true,
            label: 'Announce New Rounds'
        }
    },
    state: {
        round: 0,
        turnOrder: []
    },
    init: function() {
        on('chat:message', (msg) => {
            if (msg.type === 'api') {
                switch(msg.content.split(' ')[0]) {
                    case '!init':
                        this.rollInitiative();
                        break;
                    case '!next':
                        this.nextTurn();
                        break;
                }
            }
        });
    },
    rollInitiative: function() {
        const selected = msg.selected;
        if (selected && selected.length > 0) {
            this.state.turnOrder = selected.map(s => {
                const token = getObj('graphic', s._id);
                const roll = randomInteger(20);
                return {
                    id: s._id,
                    name: token.get('name'),
                    initiative: roll
                };
            }).sort((a, b) => b.initiative - a.initiative);
            this.state.round = 1;
            this.announceTurnOrder();
        }
    },
    nextTurn: function() {
        if (this.state.turnOrder.length > 0) {
            const current = this.state.turnOrder.shift();
            this.state.turnOrder.push(current);
            if (this.state.turnOrder[0] === current) {
                this.state.round++;
                if (mod.config.announceRounds) {
                    sendChat('Initiative Tracker', `Round ${this.state.round} begins!`);
                }
            }
            sendChat('Initiative Tracker', `It's ${current.name}'s turn!`);
        }
    },
    announceTurnOrder: function() {
        const order = this.state.turnOrder.map(t => `${t.name} (${t.initiative})`).join(', ');
        sendChat('Initiative Tracker', `Initiative order: ${order}`);
    }
};

mod.register(initiativeTrackerMod);
```

These examples demonstrate various aspects of Mod development, including:

- Basic and advanced command handling
- Using configuration options
- Manipulating game objects (tokens)
- Managing state across turns/rounds
- Interacting with Roll20's randomization functions
- Creating more complex game management systems

## API Events

The Roll20 API provides various events that you can listen to and respond to in your scripts. Events are fired synchronously in order from first-bound to last-bound, and from specific property to general object.

### Event Types

1. **Chat Events**: Triggered by chat messages.
2. **Object Events**: Triggered by changes to game objects (e.g., tokens, characters, handouts).
3. **Campaign Events**: Triggered by changes to campaign-wide settings or states.

### Callback Parameters

Event callbacks typically receive two parameters:

- `obj`: The object that was changed. Use `obj.get()` and `obj.set()` to interact with it.
- `prev`: An object containing the previous values of changed properties.

### Key Events

#### Chat Events

```javascript
on('chat:message', function(msg) {
    // Triggered when a chat message is sent
    if(msg.type == 'api' && msg.content.startsWith('!mycommand')) {
        // Handle API command
    }
});
```

#### Object Events

```javascript
on('add:graphic', function(obj) {
    // Triggered when a new token is added to the map
    log('New token added: ' + obj.get('name'));
});

on('change:attribute', function(obj, prev) {
    // Triggered when a character attribute changes
    if(obj.get('name') == 'hp') {
        log('HP changed from ' + prev['current'] + ' to ' + obj.get('current'));
    }
});

on('destroy:character', function(obj) {
    // Triggered when a character is deleted
    log('Character deleted: ' + obj.get('name'));
});
```

#### Campaign Events

```javascript
on('ready', function() {
    // Triggered when the API and game data have finished loading
    log('API Ready!');
});

on('change:campaign:playerpageid', function(obj, prev) {
    // Triggered when the player page changes
    log('Player page changed from ' + prev['playerpageid'] + ' to ' + obj.get('playerpageid'));
});

on('change:campaign:turnorder', function(obj, prev) {
    // Triggered when the turn order changes
    log('Turn order updated');
});
```

### Best Practices

1. Bind to specific events when possible (e.g., `change:graphic:left` instead of `change:graphic`) for better performance.
2. Use the `ready` event to ensure all campaign data is loaded before running your initialization code.
3. Be aware that API-triggered changes do not fire events to prevent infinite loops.
4. Handle errors gracefully to prevent script crashes.

Remember to test your event listeners thoroughly to ensure they behave as expected in various scenarios.

## API Utility Functions

Roll20 provides several utility functions to help with common tasks:

### Random Number Generation

```javascript
let d20Roll = randomInteger(20); // Returns a random integer from 1 to 20
let percentageRoll = _.random(100); // Returns a random integer from 0 to 100
```

### Player Management

```javascript
let isGM = playerIsGM(msg.playerid); // Check if a player is a GM
let onlinePlayers = findObjs({_type: 'player', _online: true}); // Get all online players
```

### Object Manipulation

```javascript
let tokenAttr = getAttrByName(characterId, 'strength'); // Get a character attribute
let pageTokens = filterObjs(function(obj) {
    return obj.get('_type') == 'graphic' && obj.get('_pageid') == Campaign().get('playerpageid');
}); // Get all tokens on the current player page
```

### Utility Functions

```javascript
on('ready', function() {
    log('Script loaded!'); // Log to the API console
    sendChat('API', 'Script is ready!'); // Send a chat message
    setTimeout(function() {
        // Do something after 5 seconds
    }, 5000);
});
```

## Mod API Settings Page

The Mod API allows you to create a settings page for your mod, making it easy for users to configure your mod without editing code.

```javascript
const myMod = {
    name: 'My Awesome Mod',
    version: '1.0',
    author: 'Your Name',
    config: {
        enableFeature: {
            type: 'checkbox',
            default: true,
            label: 'Enable Feature'
        },
        customMessage: {
            type: 'text',
            default: 'Hello World',
            label: 'Custom Message'
        },
        diceType: {
            type: 'select',
            default: 'd20',
            options: ['d4', 'd6', 'd8', 'd10', 'd12', 'd20'],
            label: 'Default Dice Type'
        }
    },
    init: function() {
        // Initialization code
    }
};

mod.register(myMod);
```

## API Debugging

Debugging API scripts can be challenging due to the sandboxed nature of the Roll20 API. Here are some techniques and tips to help diagnose problems with your scripts:

### "Caveman" Debugging

Since you don't have direct access to the environment where the scripts are being run, you can rely on copious amounts of `log` calls to tell what's going on with your program. For example:

```javascript
on("change:graphic:left", function(obj) {
   //What's the object's left value coming into this?
   log(obj.get("left"));
   obj.set("left", obj.get("left") + 70);
   //What's it now?
   log(obj.get("left"));
   //You can also debug whole objects to see a list of their current attributes
   log(obj);
});
```

You'll find the output of your log commands in the Mod (API) Console, which is on the Scripts Editor page for your Campaign.

### Error Locks

If the API detects a serious error that it can't recover from, it will put an "error lock" on your Campaign which causes your Mod (API) Scripts not to run until the error is resolved. To fix this:

1. Make changes to your scripts to try and solve the problem.
2. Click the "Save Script" button.
3. The error lock will be "cleared" and the API will attempt to run your scripts again.
4. If there is another error, the error lock will be re-applied.
5. Repeat this process as needed.

### Common Errors

1. **"myvar is not defined"**: Often caused by a typo in the name of one of your variables, such as missing a capital letter.

2. **"Cannot read property 'myProperty' or Cannot call method 'myMethod'"**: Likely due to:
   - Trying to find an object, but the result was undefined.
   - A variable being conditionally defined, but none of the conditions matched.

3. **"Unexpected token"**: You are either missing a character or have one too many characters. This can result from forgetting a comma or having incorrect parentheses.

4. **_displayname returns undefined, while get("_displayname") returns a name**: Most properties in Roll20 objects need to be accessed via the `get()` and `set()` methods. When using `get()`, omit the leading underscore on read-only properties.

### Additional Tips

1. Use `log()` extensively to output variable values and execution flow.
2. Enable the Developer Console in your browser (usually F12) to see detailed error messages.
3. Use try-catch blocks to handle errors gracefully:

```javascript
try {
    // Your code here
} catch(err) {
    log('Error: ' + err.message);
}
```

4. Use the API Console in Roll20 to see your log outputs and any error messages.
5. Test your scripts in a development campaign before deploying to your main game.

## Mod API Settings Page

The Mod API Settings Page is where you can add, change, and manipulate your Mod (API) scripts. Here's an overview of its main sections:

### 1. Script Library Section

This dropdown includes a list of all the curated scripts that Roll20 offers for one-click installation. The list is continuously updated with approved scripts. You can also install scripts from the [official Roll20 GitHub library](https://github.com/Roll20/roll20-api-scripts) by adding them manually, or create your own scripts from scratch.

Selecting a script displays additional information, including usage instructions, author, version, and other important details. Review all information before installing a script. Use the **Add Script** button to install, or the **Import** button to import a script.

### 2. New Script Section

This section allows you to add code directly into the API and save it as a script. It includes a built-in coding editor for adding and manipulating your script code. Use the **Disable Script** and **Save Script** buttons to manage your scripts. It's recommended to have a basic understanding of coding and JavaScript before making changes here.

### 3. Restart Mod (API) Sandbox Button

This button restarts the instance of the Mod (API) that is running, effectively rebooting any Mod (API) scripts and restarting any other affected processes.

### 4. Mod (API) Output Console

The Mod (API) Console is your "window" into your scripts. It displays information on script results or errors that occur during execution. All `log()` commands and any encountered errors will show here, allowing you to monitor your scripts' behavior and troubleshoot issues.

## API Token Markers

Roll20 provides functions to manipulate token markers (status markers). The token marker information is stored under the campaign node as 'token_markers' and can be accessed via the API:

```javascript
let tokenMarkers = JSON.parse(Campaign().get("token_markers"));
```

This information is read-only and returns a JSON array containing an object for each token marker currently in the game:

```javascript
{
    "id": 59, // the database id for the marker
    "name": "Bane", // the name (non-unique) of the marker
    "tag": "Bane::59", // how the token is actually referenced
        // this will include the id for custom markers, but not for default markers
    "url": "https://s3.amazonaws.com/files.d20.io/images/59/yFnKXmhLTtbMtaq-Did1Yg/icon.png?1575153187"
    // the url for the token marker's image
}
```

Here are some common operations with token markers:

```javascript
// Add a marker to a token
token.set('status_blue', true);

// Remove a marker from a token
token.set('status_red', false);

// Set a numbered marker
token.set('status_green', 3);

// Get all markers on a token
let markers = token.get('statusmarkers').split(',');

// Set a custom marker
token.set('status_custom', 'https://s3.amazonaws.com/files.d20.io/images/1234567/abcdef.png');
```

You can create useful functions to work with token markers, such as:

1. Listing all available markers
2. Finding markers by name
3. Setting markers on tokens
4. Getting markers from tokens

Here's an example script that demonstrates these operations:

```javascript
on("ready", () => {
    const tokenMarkers = JSON.parse(Campaign().get("token_markers"));

    const getChatMessageFromTokenMarkers = markers => {
        let chatMessage = '';
        _.each(markers, marker => {
            chatMessage += `<p><img src='${marker.url}'> ${marker.id}: ${marker.name}</p>`;
        });
        return chatMessage;
    };

    on("chat:message", msg => {
        if(msg.content.split(" ")[0].toLowerCase() === '!markernames') {
            let chatMessage = getChatMessageFromTokenMarkers(tokenMarkers);
            sendChat("Token Markers", chatMessage);
        } else if(msg.content.split(" ")[0].toLowerCase() === '!markerids') {
            const markerName = msg.content.split(" ")[1].toLowerCase();
            let results = [];
            _.each(tokenMarkers, marker => {
                if(marker.name.toLowerCase() === markerName) results.push(marker);
            });
            let chatMessage = getChatMessageFromTokenMarkers(results);
            chatMessage = chatMessage || 'Unable to find any matching token markers'
            sendChat("Token Markers", chatMessage);
        } else if(msg.content.split(" ")[0].toLowerCase() === '!settokenmarker') {
            const markerName = msg.content.split(" ")[1].toLowerCase();
            if (!msg.selected && msg.selected[0]._type == "graphic") return;
            obj = getObj(msg.selected[0]._type, msg.selected[0]._id);
            currentMarkers = obj.get("statusmarkers").split(',');
            currentMarkers.push(markerName);
            obj.set("statusmarkers", currentMarkers.join(','));
        } else if(msg.content.split(" ")[0].toLowerCase() === '!gettokenmarkers') {
            if (!msg.selected || msg.selected[0]._type !== "graphic") return;
            obj = getObj(msg.selected[0]._type, msg.selected[0]._id);
            currentMarkers = obj.get("statusmarkers");
            sendChat("Token Markers", currentMarkers);
        }
    });
});
```

This script adds the following chat commands:
- `!markernames`: Lists all available markers
- `!markerids <name>`: Finds markers by name
- `!settokenmarker <string>`: Adds a marker to the selected token
- `!gettokenmarkers`: Lists all markers on the selected token

Remember to always test your scripts and Mods thoroughly and handle errors gracefully to ensure a smooth experience for your players. When creating Mods, consider making them configurable and reusable to benefit the wider Roll20 community.

## API Utility Functions

The Roll20 API provides various utility functions to help you work with the game space consistently. These functions can be called from anywhere in your scripts.

### Underscore.js

The Underscore.js library is available via the `_` global object. It provides helper functions like `_.each` for iterating through arrays of objects. For more information, refer to the [Underscore documentation](http://underscorejs.org/).

### Logging

```javascript
log(message)
```

Use this function to log output to the Mod (API) console on the Script Editor page. It's useful for debugging scripts and understanding what's happening inside the Mod (API) sandbox.

Example:
```javascript
on("change:graphic", function(obj) {    
  log("Heard change for object ID: " + obj.id);
});
```

### Object Ordering

```javascript
toFront(obj)
toBack(obj)
```

These functions move an object on the tabletop to the front or back of its current layer. You must pass in an actual object, such as one received in an event callback or by calling `getObj` or `findObjs`.

### Random Numbers

```javascript
randomInteger(max)
```

Returns a random integer between 1 and `max` (inclusive). This function accounts for Modulo Bias, ensuring evenly distributed results. Use this function for dice rolls and other cases where even distribution is important.

```javascript
Math.random()
```

The default `Math.random()` in JavaScript has been replaced with Roll20's cryptographically-secure PRNG. While it provides truly random numbers, it's not suitable for generating evenly distributed numbers in a range. Use `randomInteger(max)` for those cases.

### Player Is GM

```javascript
playerIsGM(playerid)
```

Returns a boolean indicating whether a player in the game is a GM or not. This function always returns the correct answer for the current moment, even if GM status changes mid-game.

### Character

```javascript
setDefaultTokenForCharacter(character, token)
```

Sets the default token for the supplied Character Object to the details of the supplied Token Object. Both objects must already exist. This will overwrite any default token currently associated with the character.

### Special Effects (FX)

```javascript
spawnFx(x, y, type, pageid)
```

Spawns a brief effect at the location (x, y) of the specified type. If pageid is omitted or undefined, the current player page is used.

```javascript
spawnFxBetweenPoints(point1, point2, type, pageid)
```

Similar to spawnFx, but creates an effect between two points. Points should be in the format {x: 100, y: 100}.

```javascript
spawnFxWithDefinition(x, y, definitionJSON, pageid)
```

Spawns an ad-hoc custom effect using the provided JSON definition at the specified location.

### Jukebox Playlists

```javascript
playJukeboxPlaylist(playlistid)
```

Begins playing the specified playlist for everyone in the game.

```javascript
stopJukeboxPlaylist()
```

Stops any playlist that is currently playing.

### Miscellaneous

```javascript
sendPing(left, top, pageid, playerid, moveAll, visibleTo)
```

Sends a "ping" to the tabletop. You must specify the coordinates and page ID. Optional parameters include the player who performed the ping, whether to move all players' views, and which players can see or be moved by the ping.

### A Note on Distances and Grids in Roll20

In Roll20, a "unit" is always 70 pixels on the screen. By default:

- 1 unit = 5 ft
- 1 unit = 1 grid square
- Therefore, 5 ft = 1 unit = 1 square

The GM can change both the size of the grid and the scale of the distance, but 1 unit will always be 70 pixels.

## Resources

- [Official Roll20 API Documentation](https://wiki.roll20.net/API:Introduction)
- [API Cookbook](https://wiki.roll20.net/API:Cookbook)
- [Mod API Cookbook](https://help.roll20.net/hc/en-us/articles/360037772893-Mod-API-Cookbook)
- [Mod API Basic Examples](https://help.roll20.net/hc/en-us/articles/360037256814-Mod-API-Basic-Examples)
- [Mod API Advanced Examples](https://help.roll20.net/hc/en-us/articles/360037256834-Mod-API-Advanced-Examples)
- [Mod API Advanced Use Guide](https://help.roll20.net/hc/en-us/articles/360037772773-Mod-API-Advanced-Use-Guide)
- [API Sandbox Model](https://help.roll20.net/hc/en-us/articles/360037772853-API-Sandbox-Model)
- [API Function Documentation](https://help.roll20.net/hc/en-us/articles/360037772833-API-Function-Documentation)
- [API Chat](https://help.roll20.net/hc/en-us/articles/360037256754-API-Chat)
- [API Objects](https://help.roll20.net/hc/en-us/articles/360037772793-API-Objects)
- [API Events](https://help.roll20.net/hc/en-us/articles/360037772813-API-Events)
- [API Utility Functions](https://help.roll20.net/hc/en-us/articles/360037256774-API-Utility-Functions)
- [Mod API Settings Page Overview](https://help.roll20.net/hc/en-us/articles/360037772753-Mod-API-Settings-Page-Overview)
- [API Debugging](https://help.roll20.net/hc/en-us/articles/360037772873-API-Debugging)
- [API Token Markers](https://help.roll20.net/hc/en-us/articles/360041536113-API-Token-Markers)
- [Roll20 API GitHub Repository](https://github.com/Roll20/roll20-api-scripts)
- [Roll20 Community Forums](https://app.roll20.net/forum/category/46)
- [Roll20 Mods API Documentation](https://help.roll20.net/hc/en-us/articles/360037256714-Roll20-Mods-API)

## Mod API Advanced Use Guide

### The Script Editor

To edit your game scripts, click on the "Mod (API) Scripts" link in the Game Details page for your game. The Script Editor includes:

- Multiple script tabs for organization
- A script code editor
- An "Mod (API) Console" at the bottom

Saving scripts, adding new scripts, deleting scripts, or toggling scripts will restart the sandbox for your game.

### The Mod (API) Console

The Mod (API) Console displays information from your scripts, including:

- Output from `log()` commands
- Errors encountered during script execution

### Reactive Scripts: Listen to Events, Modify Objects

Reactive scripts respond to changes on the tabletop. Example:

```javascript
on("change:graphic", function(obj) {
  obj.set({
    left: obj.get("left") + distanceToPixels(5)
  });
});
```

### Utility Functions

Use utility functions like `distanceToPixels()` to make your scripts more robust:

```javascript
on("change:graphic", function(obj) {
  obj.set({
    left: obj.get("left") + distanceToPixels(5)
  });
});
```

### Proactive Scripts: Do Things Without User Intervention

Proactive scripts can perform actions automatically:

```javascript
on("ready", function() {
  var patroltoken = findObjs({_type: "graphic", name: "Guard A"})[0];
  var direction = -1 * distanceToPixels(5);
  var stepstaken = 0;
  setInterval(function() {
    if(stepstaken > 3) {
      direction *= -1;
      stepstaken = 0;
    }
    patroltoken.set("left", patroltoken.get("left") + direction);
    stepstaken++;
  }, 5000);
});
```

### Asynchronous Functions

Many Roll20 API functions are asynchronous. Example:

```javascript
on('load', function() {
  log('Before asynchronous function');
  sendChat('Async Function', 'Evaluate this: [[1d6]]', function(msg) {
    log('Inside asynchronous function');
  });
  log('After asynchronous function');
});
```

Asynchronous functions help prevent the API from becoming unresponsive.

### Best Practices

1. Use `set()` and `get()` to modify object properties
2. Utilize utility functions for consistency across different page settings
3. Handle asynchronous operations properly
4. Use the `on("ready", ...)` event to ensure the game is fully loaded before running your code
5. Implement error handling and logging for easier debugging

## API Sandbox Model

The Roll20 API runs in a sandboxed environment for security reasons. Here are some key points about the sandbox:

### Available JavaScript Features

- ECMAScript 5.1 compliant
- Some ES6 features (e.g., `let`, `const`, arrow functions)
- `setTimeout()` and `setInterval()` (with limitations)

### Limitations

- No direct DOM access
- Limited network access (only to approved URLs)
- 5-second timeout for script execution
- 500ms cooldown between API commands

### Sandbox Libraries

The sandbox includes several useful libraries:

- Underscore.js
- Cheerio (for HTML parsing)
- moment.js (for date/time manipulation)

### Security Considerations

- Always validate and sanitize user input
- Use Roll20's built-in methods for sensitive operations
- Be cautious when using external data sources

### Best Practices in the Sandbox

1. Optimize for performance to avoid hitting the 5-second timeout
2. Use Roll20's state object for persistent storage
3. Leverage built-in Roll20 objects and methods when possible
4. Handle errors gracefully to prevent script crashes

Remember that the sandbox environment is designed to protect both Roll20 and its users. Always test your Mods thoroughly in this environment before publishing or sharing them with others.

## API Sandbox Model

The Roll20 API functions by running a special server-side virtual machine for each campaign. This provides a **sandbox** where your custom scripts can run without any danger of them affecting other user's campaigns. In addition, this provides a layer of security which prevents a malicious GM from writing scripts which could do bad things like access a player's computer or stall their computer with an infinite loop.

### How it Works

If you're curious in the technical details of how the API functions, here's a brief diagram:

User-written scripts ===> API Server ===> Campaign Sandbox <===> Real-Time Sync Server

The Roll20 API Server listens for activity on your campaign. When it detects that people are using your campaign, it spins up a sandbox for your campaign and loads any Mod (API) scripts that you have written into the sandbox. The sandbox can receive and send data directly to the real-time sync server, which allows it to respond to events and make changes to the game.

### Restrictions from Normal Javascript

While Roll20 scripts are Javascript, there are some restrictions you should be aware of if you're used to programming Javascript for websites. Roll20 scripts are executed in a separate sandbox from the Roll20 site. This provides an additional layer of separation and security for our system and your players. This sandbox means that:

- You cannot make HTTP Requests (AJAX).
- You cannot load external scripts or libraries (e.g. jQuery).
- The environment is Javascript, but it is not an environment in a browser, so there is no DOM, page elements, CSS, `document`, `window`, etc.

## API Function Documentation

The Roll20 API provides a number of functions that are not part of core JavaScript or other libraries. Here are the key functions and their usage:

### Global Variables

- `_`: The Underscore.js library namespace object
- `state`: Object for persisting data between sessions

### Key Functions

#### Campaign()
Gets the singleton Campaign Roll20 object.

```javascript
var currentPageID = Campaign().get('playerpageid');
```

#### createObj(type, attributes)
Creates a new Roll20 object.

```javascript
createObj('attribute', {
    name: 'Strength',
    current: 0,
    max: 30,
    characterid: characterObj.id
});
```

#### filterObjs(callback)
Gets Roll20 objects that pass a predicate test.

```javascript
var duplicateTokens = filterObjs(function(obj) {
    return obj.get('type') === 'graphic' && obj.get('name') === tokenName;
});
```

#### findObjs(attributes, [options])
Gets Roll20 objects matching given attributes.

```javascript
var npcs = findObjs({ type: 'character', controlledby: '' });
```

#### getAllObjs()
Gets all Roll20 objects in the campaign.

```javascript
var everything = getAllObjs();
```

#### getAttrByName(characterId, attributeName, [valueType])
Gets an attribute value for a character.

```javascript
var strength = getAttrByName(character.id, 'strength');
```

#### getObj(type, id)
Gets a specific Roll20 object.

```javascript
var token = getObj('graphic', tokenId);
```

#### log(message)
Logs a message to the API console.

```javascript
log('Script loaded!');
```

#### on(event, callback)
Registers an event handler.

```javascript
on('chat:message', function(msg) {
    // Handle chat message
});
```

#### playerIsGM(playerId)
Checks if a player is a GM.

```javascript
if (playerIsGM(msg.playerid)) {
    // Execute GM-only code
}
```

#### randomInteger(max)
Generates a random integer between 1 and max (inclusive).

```javascript
var d20Roll = randomInteger(20);
```

#### sendChat(speakingAs, message, [callback], [options])
Sends a chat message.

```javascript
sendChat('API', 'Hello, world!');
```

#### spawnFx(left, top, type, [pageId])
Spawns a special effect.

```javascript
spawnFx(token.get('left'), token.get('top'), 'burst-fire');
```

#### toFront(obj)
Moves a graphic object to the front of its layer.

```javascript
toFront(tokenObj);
```

#### toBack(obj)
Moves a graphic object to the back of its layer.

```javascript
toBack(tokenObj);
```

For more detailed information and additional functions, refer to the [official Roll20 API documentation](https://help.roll20.net/hc/en-us/articles/360037772833-API-Function-Documentation).

## API Chat

The Roll20 API provides various functions for interacting with the chat system. Here are some key details:

### Chat Events

The `chat:message` event is triggered whenever a new chat message is received. The callback receives a message object with properties like `who`, `type`, `content`, etc.

### sendChat Function

The `sendChat` function allows you to send chat messages programmatically:

```javascript
sendChat(speakingAs, input [, callback [, options]])
```

- `speakingAs`: Who the message is sent as (player name, character name, etc.)
- `input`: The message content
- `callback`: Optional function to handle the results
- `options`: Optional object to set message options

### API Command Buttons

You can create clickable buttons in chat that trigger API commands:

```
[Button Label](!apicommand)
```

This creates a button that executes `!apicommand` when clicked.

## API Objects

The Roll20 API provides access to various game objects that can be manipulated programmatically. Here's an overview of key object types:

### Path

Properties include:
- _id: Unique identifier
- _type: "path"
- _path: JSON string describing the lines in the path
- fill: Fill color
- stroke: Stroke color
- layer: "gmlayer", "objects", "map", or "walls"
- width/height: Size
- top/left: Position
- controlledby: Player IDs who can control the path

### Text

Properties include:
- _id: Unique identifier
- _type: "text"
- text: The text content
- font_size: Font size (best to use preset sizes)
- color: Text color
- font_family: Font family
- layer: "gmlayer", "objects", "map", or "walls"

### Graphic (Token/Map/Card/Etc.)

Properties include:
- _id: Unique identifier
- _type: "graphic"
- _subtype: "token" or "card"
- imgsrc: URL of the image
- left/top: Position 
- width/height: Size
- layer: "objects", "gmlayer", etc.
- name: Token name
- controlledby: Player IDs who can control it
- represents: ID of the character this token represents
- bar1_value/bar2_value/bar3_value: Values for token bars
- aura1_radius/aura2_radius: Radius of auras
- statusmarkers: Active status markers

### Character 

Properties include:
- _id: Unique identifier  
- _type: "character"
- name: Character name
- controlledby: Player IDs who can edit
- inplayerjournals: Player IDs who can view
- bio: Biography text (requires callback to access)
- gmnotes: GM-only notes (requires callback to access)

### Attribute

Properties include:
- _id: Unique identifier
- _type: "attribute" 
- _characterid: ID of character it belongs to
- name: Attribute name
- current: Current value
- max: Maximum value

### Ability

Properties include:
- _id: Unique identifier
- _type: "ability"
- _characterid: ID of character it belongs to
- name: Ability name
- description: Ability description
- action: The text of the ability
- istokenaction: Whether it's a token action

### Handout

Properties include:
- _id: Unique identifier
- _type: "handout"
- name: Handout name
- notes: Handout text content (requires callback to access)
- gmnotes: GM-only notes (requires callback to access)
- inplayerjournals: Player IDs who can view
- controlledby: Player IDs who can edit

### Campaign

Properties include:
- _id: "root"
- _type: "campaign"
- turnorder: JSON string of the turn order
- playerpageid: ID of the current player page
- playerspecificpages: Object mapping player IDs to page IDs

Use functions like getObj(), findObjs(), and createObj() to work with these objects in your scripts. For example:

```javascript
// Get a character by ID
var character = getObj("character", characterId);

// Find all tokens on the current page
var currentPageTokens = findObjs({
  _pageid: Campaign().get("playerpageid"),
  _type: "graphic",
  _subtype: "token"
});

// Create a new attribute for a character
createObj("attribute", {
  name: "Strength",
  current: 10,
  max: 20,
  characterid: characterId
});
```

Note: When working with asynchronous fields like "bio", "gmnotes", or "notes", you must use a callback function:

```javascript
character.get("bio", function(bio) {
  // Do something with the bio text
});
```

Remember to always check for null values and use error handling when working with objects, as they may not always exist or be accessible depending on the game state and user permissions.

There are several different types of objects that are used throughout the Roll20 API. Here's a quick listing of each, what it is, and what properties it contains (along with the default values). As a general rule of thumb, properties that begin with an underscore (_) are read-only and cannot be changed. You must access properties on objects using obj.get("property") and set new values using obj.set("property", newvalue) or obj.set({property: newvalue, property2: newvalue2}).
Note: The id property of an object is a globally-unique ID: no two objects should have the same one, even across different types of objects. In addition, since an object's id is frequently-accessed and never changes, there is a shortcut available where you can access it by using obj.id instead of obj.get("_id") if you wish (either will work).

Path
Property	Default Value	Notes
_id	 	
A unique ID for this object. Globally unique across all
objects in this game. Read-only.

_type	"path"	Can be used to identify the object type or search for the
object. Read-only.
_pageid	  	ID of the page the object is in. Read-only.
_path	  	A JSON string describing the lines in the path. Read-only, except when creating a new path. See the section on Paths for more information.
fill	"transparent"	Fill color. Use the string "transparent" or a hex color as a string, for example "#000000"
stroke	"#000000"	Stroke (border) color.
rotation	0	Rotation (in degrees).
layer	""	Current layer, one of "gmlayer", "objects", "map", or "walls". The walls layer is used for dynamic lighting, and paths on the walls layer will block light.
stroke_width	5	 
width	0	 
height	0	 
top	0	Y-coordinate for the center of the path
left	0	X-coordinate for the center of the path
scaleX	1	 
scaleY	1	 
controlledby	""	
Comma-delimited list of player IDs who can control the path. Controlling players may delete the path. If the path was created by a player, that player is automatically included in the list.

All Players is represented by having 'all' in the list.

barrierType	"wall"	
Dynamic Lighting Barrier type options include "wall", "oneWay", and "transparent"

oneWayReversed	false	
boolean

For more information on the format of _path data, see the section on paths.

 

Window
Note: Window and Door use an inverted axis compared to other types of objects. For instance, a top variable that would be 100 for another object is y -100 for window or door.

Property	Default Value	Notes
_id	 	A unique ID for this object. Globally unique across all objects in this game. Read-only.
_type	"window"	Read-only.
color	 	A hexadecimal color of the path.
x	0	Coordinate center of the door on the x axis.
y	0	Coordinate center of the door on the y axis.
isOpen	false	Determines whether a player can move through this window.
isLocked	false	Prevents players from being able to interact with the window.
path	 	Represented as two handles (handle0 and handle1) each with x and y coordinates.
Example
on('chat:message', function(msg) {
    if (msg.type === 'api' && msg.content === '!cw') {
        const currentPageID = Campaign().get('playerpageid');
        const win = createObj('window', {
            x: 70,
            y: -70,
            pageid: currentPageID,
            path: {
		        handle0: {
        			x: -70,
        			y: 0,
        		},
        		handle1: {
        			x: 35,
        			y: 0,
        		},
        	},
            color: '#000000'
        });
    }

    if (msg.type === 'api' && msg.content === '!mw') {
        const win = getObj('window', '-NG38yUgghBBoV8YR0y1');
        win.set({
           x: 240,
           y: -139
        });
    }

    if (msg.type === 'api' && msg.content === '!dw') {
        const win = getObj('window', '-NG38yUgghBBoV8YR0y1');
        win.remove();
    }
});
Door
Note: Window and Door use an inverted axis compared to other types of objects. For instance, a top variable that would be 100 for another object is y -100 for window or door.

Property

Default Value

Notes

_id

 	
A unique ID for this object. Globally unique across all objects in this game. Read-only.

_type

"door"

Read-only.

color

 	
A hexadecimal color of the path.

x

0

Coordinate center of the door on the x axis.

y

0

Coordinate center of the door on the y axis.

isOpen

false

Determines whether a player can move through this door.

isLocked

false

Prevents players from being able to interact with the door.

isSecret

false

Removes a door icon from player view and functions as a barrier.

path

 	
Represented as two handles (handle0 and handle1) each with x and y coordinates.

Text
Property	Default Value	Notes
_id	 	A unique ID for this object. Globally unique across all objects in this game. Read-only.
_type	"text"	Can be used to identify the object type or search for the object. Read-only.
_pageid	 	ID of the page the object is in. Read-only.
top	0	 
left	0	 
width	0	 
height	0	 
text	""	 
font_size	16	For best results, stick to the preset sizes in the editing menu: 8, 10, 12, 14, 16, 18, 20, 22, 26, 32, 40, 56, 72, 100, 200, 300.
rotation	0	 
color	"rgb(0, 0, 0)"	 
font_family	"Arial"	If this is not set, when later changing the value of the "text" property the font_size will shrink to 8. Possible values (Case is not important): "Arial", "Patrick Hand", "Contrail One", "Shadows Into Light", and "Candal". Specifying an invalid name results in an unnamed, monospaced serif font being used.
layer	""	"gmlayer", "objects", "map", or "walls".
controlledby	""	Comma-delimited list of player IDs who can control the text. Controlling players may delete the text. If the text was created by a player, that player is automatically included in the list.
All Players is represented by having 'all' in the list.

Graphic (Token/Map/Card/Etc.)
Property	Default Value	Notes
_id	 	A unique ID for this object. Globally unique across all objects in this game. Read-only.
_type	"graphic"	Can be used to identify the object type or search for the object. Read-only.
_subtype	"token"	May be "token" (for tokens and maps) or "card" (for cards). Read-only.
_cardid	 	Set to an ID if the graphic is a card. Read-only.
_pageid	 	ID of the page the object is in. Read-only.
imgsrc	 	The URL of the graphic's image. See the note about imgsrc and avatar restrictions below.
bar1_link	 	Set to an ID if Bar 1 is linked to a character.
bar2_link	 	 
bar3_link	 	 
represents	 	ID of the character this token represents.
left	0	Number of pixels from the left edge of the map to the center of the graphic.
top	0	Number of pixels from the top edge of the map to the center of the graphic.
width	0	Width of the graphic, in pixels.
height	0	Height of the graphic, in pixels.
rotation	0	The orientation of the token in degrees.
layer	""	"gmlayer", "objects", "map", or "walls".
isdrawing	false	This property is changed from the Advanced context menu.
flipv	false	Flip vertically.
fliph	false	Flip horizontally.
name	""	The token's name.
gmnotes	""	Notes on the token only visible to the GM.
controlledby	""	Comma-delimited list of player IDs who can control the graphic. Controlling players may delete the graphic. If the graphic was created by a player, that player is automatically included in the list.
All Players is represented by having 'all' in the list.

bar1_value	""	Current value of Bar 1. This may be a number or text.
bar2_value	""	 
bar3_value	""	 
bar1_max	""	Maximum value of Bar 1. If _value and _max are both set, a bar may be displayed above the token showing the percentage of Bar 1.
bar2_max	""	 
bar3_max	""	 
aura1_radius	""	Radius of the aura, using the units set in the page's settings. May be an integer or a float. Set to the empty string to clear the aura.
aura2_radius	""	 
aura1_color	"#FFFF99"	A hexadecimal color or the aura.
aura2_color	"#59E594"	 
aura1_square	false	Is the aura a circle or a square?
aura2_square	false	 
tint_color	"transparent"	Hexadecimal color, or "transparent". Will tint the color of the graphic.
statusmarkers	""	A comma-delimited list of currently active statusmarkers. See the notes below for more information.
token_markers	""	A stringified JSON array containing an object for each token marker currently in the game:. You can find an example below.
showname	false	Whether the token's nameplate is shown.
showplayers_name	false	Show the nameplate to all players.
showplayers_bar1	false	Show Bar 1 to all players.
showplayers_bar2	false	 
showplayers_bar3	false	 
showplayers_aura1	false	Show Aura 1 to all players.
showplayers_aura2	false	 
playersedit_name	true	Allow controlling players to edit the token's name. Also shows the nameplate to controlling players, even if showplayers_name is false.
playersedit_bar1	true	Allow controlling players to edit the token's Bar 1. Also shows Bar 1 to controlling players, even if showplayers_bar1 is false.
playersedit_bar2	true	 
playersedit_bar3	true	 
playersedit_aura1	true	Allow controlling players to edit the token's Aura 1. Also shows Aura 1 to controlling players, even if showplayers_aura1 is false.
playersedit_aura2	true	 
light_radius	""	Dynamic lighting radius.
light_dimradius	""	Start of dim light radius. If light_dimradius is the empty string, the token will emit bright light out to the light_radius distance. If light_dimradius has a value, the token will emit bright light out to the light_dimradius value, and dim light from there to the light_radius value.
light_otherplayers	false	Show the token's light to all players.
light_hassight	false	The light has "sight" for controlling players for the purposes of the "Enforce Line of Sight" setting.
light_angle	"360"	Angle (in degrees) of the light's angle. For example, "180" means the light would show only for the front "half" of the "field of vision".
light_losangle	"360"	Angle (in degrees) of the field of vision of the graphic (assuming that light_hassight is set to true)
lastmove	""	The last move of the token. It's a comma-delimited list of coordinates. For example, "300,400" would mean that the token started its last move at left=300, top=400. It's always assumed that the current top + left values of the token are the "ending point" of the last move. Waypoints are indicated by multiple sets of coordinates. For example, "300,400,350,450,400,500" would indicate that the token started at left=300, top=400, then set a waypoint at left=350, top=450, another waypoint at left=400, top=500, and then finished the move at its current top + left coordinates.
light_multiplier	"1"	Multiplier on the effectiveness of light sources. A multiplier of two would allow the token to see twice as far as a token with a multiplier of one, with the same light source.
adv_fow_view_distance	""	The radius around a token where Advanced Fog of War is revealed.
light_sensitivity_multiplier	100	Multiplier on the effectiveness of light sources. A multiplier of 200 would allow the token to see twice as far as a token with a multiplier of 100, with the same light source.
night_vision_effect
 	Changes the Night Vision Effect. Other options include "Dimming" and "Nocturnal"
bar_location	 	Adjusts the location of the token bars. Options include 'overlap_top', 'overlap_bottom','bottom'
compact_bar
 	Adjusts whether the bar is compact or not. Other option is compact.
lockMovement	false	An option to lock a Graphic in place. Boolean true or false value
Token Markers Example
{
          "id":59, // the database id for the
          "name":"Bane", // the name (non-unique) of the marker
          "tag":"Bane::59", // how the token is actually referenced
          // this will include the id for custom markers, but not
          // for default markers.
          "url":"https://s3.amazonaws.com/files.d20.io/images/59/yFnKXmhLTtbMtaq-Did1Yg/icon.png?1575153187"

          // ^the url for the token marker's image
          }
Important Notes About Linked Characters + Tokens
Note that for tokens that are linked to Characters, the controlledby field on the token is overridden by the controlledby field on the Character.

For token bars (e.g. bar1_value and bar1_max) where the token is linked to an Attribute (e.g. bar1_link is set), setting a value to the bar will automatically update the underlying Attribute's current and/or max values as well, so you don't have to set both manually.

In addition, when the Attribute (or token bar) is modified in-game, you will hear a change:attribute (and property-specific, e.g. change:attribute:current) event, followed by a change:graphic (and change:graphic:bar1_value) event. You can choose to respond to either event, but the underlying bar values will not yet be updated when the attribute event fires, since it fires first.

Important Notes About Status Markers
As of August 6, 2013 the way that status markers on tokens are handled has changed. The "statusmarkers" property of the Graphic object is now a comma-delimited list of all status marker colors/icons that should be active on the token. The format is as follows:

//Comma-delimited (use join to create or split to turn into an array). 
//If a status icon/color is followed by an "@" symbol, the number after 
//"@" will be shown as the badge on the icon
statusmarkers = "red,blue,skull,dead,brown@2,green@6"
While you can access the statusmarkers property directly, to maintain backward-compatibility with existing scripts, and to provide an easy way to work with the status markers without needing to write code to handle splitting up and parsing the string yourself, we provide a set of "virtual" properties on the object that you can set/get to work with the status markers. Each status marker has a "status_<markername>" property. For example:

obj.get("status_red"); //Will return false if the marker is not active, true if it is, and a string (e.g. "2" or "5") if there is currently a badge set on the marker
obj.get('status_bluemarker'); //Is still supported for backwards compatability, and is equivalent to doing obj.get("status_blue");
obj.set("status_red", false); //would remove the marker
obj.set("status_skull", "2"); //would set a badge of "2" on the skull icon, and add it to the token if it's not already active.
Note that these virtual properties do not have events, so you must use change:graphic:statusmarkers to listen for changes to the status markers of a token, and for example change:graphic:status_red is NOT a valid event and will never fire.

The full list of status markers that are available (in the same order they appear in the marker tray):

"red", "blue", "green", "brown", "purple", "pink", "yellow", "dead", "skull", "sleepy", "half-heart", "half-haze", "interdiction", "snail", "lightning-helix", "spanner", "chained-heart", "chemical-bolt", "death-zone", "drink-me", "edge-crack", "ninja-mask", "stopwatch", "fishing-net", "overdrive", "strong", "fist", "padlock", "three-leaves", "fluffy-wing", "pummeled", "tread", "arrowed", "aura", "back-pain", "black-flag", "bleeding-eye", "bolt-shield", "broken-heart", "cobweb", "broken-shield", "flying-flag", "radioactive", "trophy", "broken-skull", "frozen-orb", "rolling-bomb", "white-tower", "grab", "screaming", "grenade", "sentry-gun", "all-for-one", "angel-outfit", "archery-target"
Page
Property	Default Value	Notes
_id	 	A unique ID for this object. Globally unique across all objects in this game. Read-only.
_type	"page"	Can be used to identify the object type or search for the object. Read-only.
_zorder	""	Comma-delimited list of IDs specifying the ordering of objects on the page. toFront and toBack (and their associated context menu items) can re-order this list. Read-only.
name	""	Page's title.
showgrid	true	Show the grid on the map.
showdarkness	false	Show fog of war on the map.
showlighting	false	Use dynamic lighting.
width	25	Width in units.
height	25	Height in units.
snapping_increment	1	Size of a grid space in units.
grid_opacity	0.5	Opacity of the grid lines.
fog_opacity	0.35	Opacity of the fog of war for the GM.
background_color	"#FFFFFF"	Hexadecimal color of the map background.
gridcolor	"#C0C0C0"	Hexadecimal color of the grid lines.
grid_type	"square"	One of "square", "hex", or "hexr". (hex corresponds to Hex(V), and hexr corresponds to Hex(H))
scale_number	5	The distance of one unit.
scale_units	"ft"	The type of units to use for the scale.
gridlabels	false	Show grid labels for hexagonal grid.
diagonaltype	"foure"	One of "foure", "pythagorean" (Euclidean), "threefive", or "manhattan".
archived	false	Whether the page has been put into archive storage.
lightupdatedrop	false	Only update Dynamic Lighting when an object is dropped.
lightenforcelos	false	Enforce Line of Sight for objects.
lightrestrictmove	false	Don't allow objects that have sight to move through Dynamic Lighting walls.
lightglobalillum	false	If true anywhere a token can "see" it is assumed there is bright light present.
jukeboxtrigger	 	Controls the Page Play on Load. Options include 'nonestopall' or the id-of-the-track
Campaign
Property	Default Value	Notes
_id	"root"	A unique ID for this object. Globally unique across all objects in this game. Read-only.
_type	"campaign"	Can be used to identify the object type or search for the object — however, note that there is only one Campaign object, and it can be accessed via Campaign(). Read-only.
turnorder	""	A JSON string of the turn order. See below.
initiativepage	false	ID of the page used for the tracker when the turn order window is open. When set to false, the turn order window closes.
playerpageid	false	ID of the page the player bookmark is set to. Players see this page by default, unless overridden by playerspecificpages below.
playerspecificpages	false	An object (NOT JSON STRING) of the format: {"player1_id": "page_id", "player2_id": "page_id" ... } Any player set to a page in this object will override the playerpageid.
_journalfolder	""	A JSON string which contains data about the folder structure of the game. Read-only.
_jukeboxfolder	""	A JSON string which contains data about the jukebox playlist structure of the game. Read-only.
 Turn Order

The turn order is a JSON string representing the current turn order listing. It is an array of objects. Currently, the turn order can only contain objects from one page at a time -- the current Page ID for the turn order is the "initiativepage" attribute. Be sure to keep them both in-sync or you may end up with strange results.

To work with the turn order, you will want to use JSON.parse() to get an object representing the current turn order state (NOTE: Check to make sure it's not an empty string "" first...if it is, initialize it yourself with an empty array). Here's an example turn order object:

[
    {
     "id":"36CA8D77-CF43-48D1-8682-FA2F5DFD495F", //The ID of the Graphic object. If this is set, the turn order list will automatically pull the name and icon for the list based on the graphic on the tabletop.
     "pr":"0", //The current value for the item in the list. Can be a number or text.
     "custom":"" //Custom title for the item. Will be ignored if ID is set to a value other than "-1".
    },
    {
     "id":"-1", //For custom items, the ID MUST be set to "-1" (note that this is a STRING not a NUMBER.
     "pr":"12",
     "custom":"Test Custom" //The name to be displayed for custom items.
    }
]
To modify the turn order, edit the current turn order object and then use JSON.stringify() to change the attribute on the Campaign. Note that the ordering for the turn order in the list is the same as the order of the array, so for example push() adds an item onto the end of the list, unshift() adds to the beginning, etc.

var turnorder;
if(Campaign().get("turnorder") == "") turnorder = []; //NOTE: We check to make sure that the turnorder isn't just an empty string first. If it is treat it like an empty array.
else turnorder = JSON.parse(Campaign().get("turnorder"));

//Add a new custom entry to the end of the turn order.
turnorder.push({
    id: "-1",
    pr: "15",
    custom: "Turn Counter"
});
Campaign().set("turnorder", JSON.stringify(turnorder));
 
Player
Property	Default Value	Notes
_id	 	A unique ID for this object. Globally unique across all objects in this game. Read-only.
_type	"player"	Can be used to identify the object type or search for the object. Read-only.
_d20userid	 	User ID — site-wide. For example, the player's user page on the wiki is /User:ID, where ID is the same value stored in _d20userid. Read-only.
_displayname	""	The player's current display name. May be changed from the user's settings page. Read-only.
_online	false	Read-only.
_lastpage	""	The page id of the last page the player viewed as a GM. This property is not updated for players or GMs that have joined as players. Read-only.
_macrobar	""	Comma-delimited string of the macros in the player's macro bar. Read-only.
speakingas	""	The player or character ID of who the player has selected from the "As" dropdown. When set to the empty string, the player is speaking as him- or herself. When set to a character, the value is "character|ID", where ID is the character's ID. When the GM is speaking as another player, the value is "player|ID", where ID is the player's ID.
color	"#13B9F0"	The color of the square by the player's name, as well as the color of their measurements on the map, their ping circles, etc.
showmacrobar	false	Whether the player's macro bar is showing.
Macro
Property	Default Value	Notes
_id	 	A unique ID for this object. Globally unique across all objects in this game. Read-only.
_type	"macro"	Can be used to identify the object type or search for the object. Read-only.
_playerid	 	The ID of the player that created this macro. Read-only.
name	""	The macro's name.
action	""	The text of the macro.
visibleto	""	Comma-delimited list of player IDs who may view the macro in addition to the player that created it.
All Players is represented by having 'all' in the list.

istokenaction	false	Is this macro a token action that should show up when tokens are selected?
 

Rollable Table
Property	Default Value	Notes
_id	 	A unique ID for this object. Globally unique across all objects in this game. Read-only.
_type	"rollabletable"	Can be used to identify the object type or search for the object. Read-only.
name	"new-table"	 
showplayers	true	 
Table Item 
Property	Default Value	Notes
_id	 	A unique ID for this object. Globally unique across all objects in this game. Read-only.
_type	"tableitem"	Can be used to identify the object type or search for the object. Read-only.
_rollabletableid	""	ID of the table this item belongs to. Read-only.
avatar	""	URL to an image used for the table item. See the note about avatar and imgsrc restrictions below.
name	""	 
weight	1	Weight of the table item compared to the other items in the same table. Simply put, an item with weight 3 is three times more likely to be selected when rolling on the table than an item with weight 1.
Character
Property	Default Value	Notes
_id	 	A unique ID for this object. Globally unique across all objects in this game. Read-only.
_type	"character"	Can be used to identify the object type or search for the object. Read-only.
avatar	""	URL to an image used for the character. See the note about avatar and imgsrc restrictions below.
name	""	 
bio	""	The character's biography. See the note below about accessing the Notes, GMNotes, and bio fields.
gmnotes	""	Notes on the character only viewable by the GM. See the note below about accessing the Notes, GMNotes, and bio fields.
archived	false	 
inplayerjournals	""	Comma-delimited list of player ID who can view this character. Use "all" to give all players the ability to view.
All Players is represented by having 'all' in the list.

controlledby	""	Comma-delimited list of player IDs who can control and edit this character. Use "all" to give all players the ability to edit.
All Players is represented by having 'all' in the list.

_defaulttoken	""	A JSON string that contains the data for the Character's default token if one is set. Note that this is a "blob" similar to "bio" and "notes", so you must pass a callback function to get(). Read-only.
Attribute
Property	Default Value	Notes
_id	 	A unique ID for this object. Globally unique across all objects in this game. Read-only.
_type	"attribute"	Can be used to identify the object type or search for the object. Read-only.
_characterid	""	ID of the character this attribute belongs to. Read-only. Mandatory when using createObj.
name	"Untitled"	 
current	""	The current value of the attribute can be accessed in chat and macros with the syntax @{Character Name|Attribute Name} or in abilities with the syntax @{Attribute Name}.
max	""	The max value of the attribute can be accessed in chat and macros with the syntax @{Character Name|Attribute Name|max} or in abilities with the syntax @{Attribute Name|max}.
 Important: See the note below about working with Character Sheets for information on how Character Sheet default values affect the use of Attributes.

Ability
Property	Default Value	Notes
_id	 	A unique ID for this object. Globally unique across all objects in this game. Read-only.
_type	"ability"	Can be used to identify the object type or search for the object. Read-only.
_characterid	""	The character this ability belongs to. Read-only. Mandatory when using createObj.
name	"Untitled_Ability"	 
description	""	The description does not appear in the character sheet interface.
action	""	The text of the ability.
istokenaction	false	Is this ability a token action that should show up when tokens linked to its parent Character are selected?
Handout
Property	Default Value	Notes
_id	 	A unique ID for this object. Globally unique across all objects in this game. Read-only.
_type	"handout"	Can be used to identify the object type or search for the object. Read-only.
avatar	""	URL to an image used for the handout. See the note about avatar and imgsrc restrictions below.
name	"Mysterious Note"	 
notes	""	Contains the text in the handout. See the note below about using Notes and GMNotes.
gmnotes	""	Contains the text in the handout that only the GM sees. See the note below about using Notes and GMNotes.
inplayerjournals	""	Comma-delimited list of player ID who can see this handout. Use "all" to display to all players.
All Players is represented by having 'all' in the list.

archived	false	 
controlledby	""	Comma-delimited list of player IDs who can control and edit this handout.
All Players is represented by having 'all' in the list.

Note: The API does not have access to the folder hierarchy. API created handouts will be placed at the root level.

Deck
Note there are helper API methods to "draw", "deal", or "shuffle" cards from the Deck. See API Update forum post from March 2018.

Property	Default Value	Notes
_id	""	id of the deck
_type	"deck"	 
name	""	name of the deck
_currentDeck	""	a comma-delimited list of cards which are currently in the deck (including those which have been played to the tabletop/hands). Changes when the deck is shuffled.
_currentIndex	-1	the current index of our place in the deck, 'what card will be drawn next?'
_currentCardShown	true	show the current card on top of the deck
showplayers	true	show the deck to the players
playerscandraw	true	can players draw cards?
avatar	""	the 'back' of the cards for this deck
shown	false	show the deck on the gameboard (is the deck currently visible?)
players_seenumcards	true	can players see the number of cards in other player's hands?
players_seefrontofcards	false	can players see the fronts of cards when looking in other player's hands?
gm_seenumcards	true	can the GM see the number of cards in each player's hand?
gm_seefrontofcards	false	can the GM see the fronts of cards when looking in each player's hand?
infinitecards	false	are there an 'infinite' number of cards in this deck?
_cardSequencer	-1	internally used to advance the deck when drawing cards.
cardsplayed	"faceup"	how are cards from this deck played to the tabletop? 'faceup' or 'facedown'.
defaultheight	""	what's the default height for cards played to the tabletop?
defaultwidth	""	 
discardpilemode	"none"	what type of discard pile does this deck have? 'none' = no discard pile, 'choosebacks' = allow players to see backs of cards and choose one, 'choosefronts' = see fronts and choose, 'drawtop' = draw the most recently discarded card, 'drawbottom' = draw the oldest discarded card.
_discardPile	""	what's the current discard pile for this deck? comma-delimited list of cards. These are cards which have been removed from play and will not be put back into the deck on a shuffle until a recall is performed.
Card
Property	Default Value	Notes
name	""	Name of the card
avatar	""	Front of the card
_deckid	""	ID of the deck
_type	"card"	 
_id	""	 
Hand
Note that each player should only have ONE hand.

Property	Default Value	Notes
currentHand	""	comma-delimited list of cards currently in the hand. Note that this is no longer read only. Ideally, it should only be adjusted with the card deck functions.
_type	"hand"	 
_parentid	""	ID of the player to whom the hand belongs
_id	""	 
currentView	"bydeck"	when player opens hand, is the view 'bydeck' or 'bycard'?
Jukebox Track
Property	Default Value	Notes
_id	 	A unique ID for this object. Globally unique across all objects in this game. Read-only.
_type	"jukeboxtrack"	Can be used to identify the object type or search for the object. Read-only.
playing	false	Boolean used to determine whether or not the track is playing. Setting this to "true" and softstop to "false" plays a track.
softstop	false	Boolean used to determine whether or not a non-looped track has finished at least once. This must be set to "false" to ensure that a track will play.
title	""	The visible label for the track in the jukebox tab.
volume	30	The volume level of the track. Note that this must be set to an integer (not a string), or you may break functionality. Values from 0-100 (percentage).
loop	false	Should the track be looped? Set to true if so.
Custom FX
Property	Default Value	Notes
_id	 	A unique ID for this object. Globally unique across all objects in this game. Read-only.
_type	"custfx"	Can be used to identify the object type or search for the object. Read-only.
name	""	The visible name for the FX in the FX Listing.
definition	{}	Javascript object describing the FX.
imgsrc and avatar property restrictions
While you can now edit the imgsrc and avatar properties, in order to provide safety to all Roll20's users we have put the following restrictions in place for those properties:

You must use an image file that has been uploaded to your Roll20 Library -- not an external site (such as Imgur), and not the Roll20 Marketplace. It will begin with 'https://s3.amazonaws.com/files.d20.io/images/' for images uploaded to the Main server, or 'https://s3.amazonaws.com/files.staging.d20.io/images/' for images uploaded to the Dev Server. You can view an image's source URL using the developer tools of your browser.
You must include the query string in the URL -- for example 'https://s3.amazonaws.com/files.staging.d20.io/images/123456/med.png?12345678', not just 'https://s3.amazonaws.com/files.staging.d20.io/images/123456/med.png'
For Graphic objects (tokens), you must use the "thumb" size of the image. It should look like 'https://s3.amazonaws.com/files.staging.d20.io/images/123456/thumb.png?12345678'.

In the future we may add a tool so that images can be uploaded specifically for use with Mod (API) scripts, but for now just use images uploaded to your own library. Note that if you delete an image from your library, it will be removed from all Games which use that image, including Games using your Mod (API) scripts.

Using the Notes, GMNotes, and Bio fields Asynchronous
In order to access the "notes", "gmnotes", or "bio" fields on Characters and Handouts, you must pass a callback function as the second argument to the get() function. Here's an example:

var character = getObj("character", "-JMGkBaMgMWiQdNDwjjS");
character.get("bio", function(bio) {
    log(bio); //do something with the character bio here.
});
You can set the value of these fields as normal. Note that there is currently (as at 2016/05/09) a bug with these asynchronous fields, whereby setting them by passing values to createObj fails quietly, leaving the object in a strange state. You should only set these values using .set until this issue is resolved. Details on the Forum. There is also a bug (as of 2016/11/05) where attempting to set both the notes and gmnotes properties in the same set() call results in the second property in the call being set erroneously. Details on the Forum.

Working with Character Sheets
The Character Sheets feature affects the usage of the Attributes object type, because the sheets have the capability of specifying a default value for each attribute on the sheet. However, if the attribute is set to the default value, there is not yet an actual Attribute object created in the game for that Character. We provide a convenience function which hides this complexity from you. You should use this function to get the value of an attribute going forward, especially if you know that a game is using a Character Sheet.

getAttrByName(character_id, attribute_name, value_type)

Simply specify the character's ID, the name (not ID) of the attribute (e.g. "HP" or "Str"), and then if you want the "current" or "max" for value_type. Here's an example:

var character = getObj("character", "-JMGkBaMgMWiQdNDwjjS");
getAttrByName(character.id, "str"); // the current value of str, for example "12"
getAttrByName(character.id, "str", "max"); //the max value of str, for example "[[floor(@{STR}/2-5)]]"

Note that fields which have auto-calculated values will return the formula rather than the result of the value. You can then pass that formula to sendChat() to use the dice engine to calculate the result for you automatically.

Be sure to also look at the Character Sheet documentation for more information on how the Character Sheets interact with the API.

getAttrByName will only get the value of the attribute, not the attribute object itself. If you wish to reference properties of the attribute other than "current" or "max", or if you wish to change properties of the attribute, you must use one of the other functions above, such as findObjs.

In the case that the requested attribute does not exist, getAttrByName() will return undefined.

Creating Objects
createObj(type, attributes)
Note: currently you can create 'graphic', 'text', 'path', 'character', 'ability', 'attribute', 'handout', 'rollabletable', 'tableitem', and 'macro' objects.

You can create a new object in the game using the createObj function. You must pass in the type of the object (one of the valid _type properties from the objects list above), as well as an attributes object containing a list of properties for the object. Note that if the object is has a parent object (for example, attributes and abilities belong to characters, graphics, texts, and paths belong to pages, etc.), you must pass in the ID of the parent in the list of properties (for example, you must include the characterid property when creating an attribute). Also note that even when creating new objects, you can't set read-only properties, they will automatically be set to their default value. The one exception to this is when creating a Path, you must include the 'path' property, but it cannot be modified once the path is initially created.

createObj will return the new object, so you can continue working with it.

//Create a new Strength attribute on any Characters that are added to the game.
on("add:character", function(obj) {
    createObj("attribute", {
        name: "Strength",
        current: 0,
        max: 30,
        characterid: obj.id
    });
});
Deleting Objects
object.remove()
Note: currently you can delete 'graphic', 'text', 'path', 'character', 'ability', 'attribute', 'handout', 'rollabletable', 'tableitem', and 'macro' objects.

You can delete existing game objects using the .remove() function. The .remove() function works on all of the objects you can create with the createObj function. You call the function directly on the object. For example, mycharacter.remove();.

Global Objects
There are several objects that are globally available anywhere in your script.

Campaign() (function)
A function which returns the Campaign object. Since there is only one campaign, this global always points to the only campaign in the game. Useful for doing things like checking to see if an object is on the active page using Campaign().get("playerpageid").

state
The state variable is an object in the global scope which is accessible to all scripts running in a game. You can access the state object from any function or callback at any time just by using the global variable named state. Additionally, the state object is persisted between executions of the Sandbox, so you can use it to store information you want to have in future runs of your script.

Note: You should use the state object to store information that is only needed by the API, since it is not sent to player computers and does not make your game file larger. Store values that are needed in-game in the Roll20 objects' properties.

Storable Types
The state object is only capable of persisting simple data types, as supported by the JSON standard.

Type	Examples	Description
Boolean	true false	The value true or false.
Number	123.5 10 1.23e20	Any number format supported by Javascript. Floating-Point or Integer.
String	'Hello Fantasy' "oh, and World"	A standard string of text.
Array	[ 1, 2, 3, 4 ] [ 'A','B','C'][1, 2, ['bob', 3], 10, 2.5]	An ordered collection of any of the types, including other arrays.
Object	{ key: 1, value: 'roll20' }	A simple key/value object with string keys and any of the types as a value, including other objects.
Warning: While functions will appear to work when stored in the state initially, they will disappear the first time the state is restored from persistence, such as on a sandbox restart.

Note: This includes Roll20 objects which you get from events or the functions findObjs(), getObj(), filterObjs(), createObj(), etc.
Important Reminders
The state object is shared between all of the scripts in a sandbox. To avoid breaking other scripts, it is important to follow a few simple guidelines:

Never assign directly to the root state object.
state = { break: 'all the things' };  // NEVER DO THIS!!!
 

Avoid using local variables named state in your scripts. While this will work, it will be confusing to later users of your scripts and could cause issues if the code is carelessly edited.
function turn(){
    var state = Campaign().get('turnorder');  // Bad Practice, Avoid it!
    // ...
}
 

Always place your properties beneath at least one namespace property. Be sure to use a sufficiently descriptive namespace property. Avoid names like script or settings. It's best to either use the name of your module or your own name or handle.
if( ! state.MyModuleNamespace ) {
    state.MyModuleNamespace = { module: 'my module', ok: 'this is fine!', count: 0 };
}
state.MyModuleNamespace.count++;
Example Usage
This is a working example that uses the state object appropriately.

on('ready',function() {
    "use strict";

    // Check if the namespaced property exists, creating it if it doesn't
    if( ! state.MyModuleNS ) {
        state.MyModuleNS = {
            version: 1.0,
            config: {
                color1: '#ff0000',
                color2: '#0000ff'
            },
            count: 0
        };
    }

    // Using the state properties to configure a message to the chat. 
    sendChat(
        'Test Module',
        '<span style="color: '+state.MyModuleNS.config.color1+';">'+
            'State test'+
        '</span> '+
        '<span style="color: '+state.MyModuleNS.config.color2+';">'+
            'Script v'+state.MyModuleNS.version+' started '+(++state.MyModuleNS.count)+' times!'+
        '</span>'
    );
});
Finding/Filtering Objects
The API provides several helper functions which can be used to find objects.

getObj(type, id)
This function gets a single object if pass in the _type of the object and the _id. It's best to use this function over the other find functions whenever possible, as its the only one that doesn't have to iterate through the entire collection of objects.

on("change:graphic:represents", function(obj) {
    if(obj.get("represents") != "") {
       var character = getObj("character", obj.get("represents"));
    }
});
 

findObjs(attrs)
Pass this function a list of attributes, and it will return all objects that match as an array. Note that this operates on all objects of all types across all pages -- so you probably want to include at least a filter for _type and _pageid if you're working with tabletop objects.

var currentPageGraphics = findObjs({                              
  _pageid: Campaign().get("playerpageid"),                              
  _type: "graphic",                          
});
_.each(currentPageGraphics, function(obj) {    
  //Do something with obj, which is in the current page and is a graphic.
});
You can also pass in an optional second argument which contains an object with a list of options, including:

caseInsensitive (true/false): If true, string properties will be compared without regard for the case of the string
var targetTokens = findObjs({
    name: "target"
}, {caseInsensitive: true});
//Returns all tokens with a name of 'target', 'Target', 'TARGET', etc.
filterObjs(callback)
Will execute the provided callback function on each object, and if the callback returns true, the object will be included in the result array. Currently, it is inadvisable to use filterObjs() for most purposes – due to the fact that findObjs() has some built-in indexing for better executing speed, it is almost always better to use findObjs() to get objects of the desired type first, then filter them using the native .filter() method for arrays.

var results = filterObjs(function(obj) {    
  if(obj.get("left") < 200 && obj.get("top") < 200) return true;    
  else return false;
});
//Results is an array of all objects that are in the top-left corner of the tabletop.
getAllObjs()
Returns an array of all the objects in the Game (all types). Equivalent to calling filterObjs and just returning true for every object.

getAttrByName(character_id, attribute_name, value_type)
Gets the value of an attribute, using the default value from the character sheet if the attribute is not present. value_type is an optional parameter, which you can use to specify "current" or "max".

getAttrByName will only get the value of the attribute, not the attribute object itself. If you wish to reference properties of the attribute other than "current" or "max", or if you wish to change properties of the attribute, you must use one of the other functions above, such as findObjs.

For repeating sections, you can use the format repeating_section_$n_attribute, where n is the repeating row number (starting with zero). For example, repeating_spells_$2_name will return the value of name from the third row of repeating_spells.

You can achieve behavior equivalent to getAttrByNamewith the following:

// current and max are completely dependent on the attribute and game system
// in question; there is no function available for determining them automatically
function myGetAttrByName(character_id,
                         attribute_name,
                         attribute_default_current,
                         attribute_default_max,
                         value_type) {
    attribute_default_current = attribute_default_current || '';
    attribute_default_max = attribute_default_max || '';
    value_type = value_type || 'current';

    var attribute = findObjs({
        type: 'attribute',
        characterid: character_id,
        name: attribute_name
    }, {caseInsensitive: true})[0];
    if (!attribute) {
        attribute = createObj('attribute', {
            characterid: character_id,
            name: attribute_name,
            current: attribute_default_current,
            max: attribute_default_max
        });
    }

    if (value_type == 'max') {
        return attribute.get('max');
    } else {
        return attribute.get('current');
    }
}

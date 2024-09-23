// NPC Creation Script for Roll20 Sandbox

const createNPC = (function() {
    'use strict';

    function handleInput(msg) {
        if (msg.type !== "api" || !msg.content.startsWith("!create-npc")) return;

        try {
            const npcData = extractNPCData(msg.content);
            if (!validateNPCData(npcData)) {
                sendChat("NPC Creator", "/w gm Error: Invalid NPC data format. Please check all required fields are present.");
                return;
            }

            const character = createObj("character", {
                name: npcData.name,
                controlledby: msg.playerid
            });

            addAttributesToCharacter(character, npcData);
            createActionsAbility(character, npcData.actions);
            createBackgroundAbility(character, npcData);
            sendChat("NPC Creator", `/w gm NPC ${npcData.name} has been created!`);
        } catch (error) {
            sendChat("NPC Creator", `/w gm Error creating NPC: ${error.message}`);
            log(`NPC Creation Error: ${error.message}`);
        }
    }

    function extractNPCData(content) {
        const jsonStr = content.replace("!create-npc", "").trim();
        try {
            return JSON.parse(jsonStr);
        } catch (error) {
            throw new Error(`Invalid JSON format. Please check your input. Error: ${error.message}`);
        }
    }

    function validateNPCData(data) {
        const requiredFields = [
            "name", "race", "class", "level", 
            "strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma",
            "actions", "background", "personality_traits", "equipment", "skills", "languages", "appearance"
        ];
        return requiredFields.every(field => data.hasOwnProperty(field));
    }

    function addAttributesToCharacter(character, data) {
        const attributes = [
            {name: "race", current: data.race},
            {name: "class", current: data.class},
            {name: "level", current: data.level},
            {name: "strength", current: data.strength},
            {name: "dexterity", current: data.dexterity},
            {name: "constitution", current: data.constitution},
            {name: "intelligence", current: data.intelligence},
            {name: "wisdom", current: data.wisdom},
            {name: "charisma", current: data.charisma}
        ];

        const repeatingAttributes = [
            {name: "equipment", items: data.equipment},
            {name: "skills", items: data.skills},
            {name: "languages", items: data.languages}
        ];

        // Add basic attributes
        attributes.forEach(attr => {
            createObj("attribute", {
                name: attr.name,
                current: attr.current,
                characterid: character.id
            });
        });

        // Add repeating attributes
        repeatingAttributes.forEach(attr => {
            attr.items.forEach((item, index) => {
                createObj("attribute", {
                    name: `repeating_${attr.name}_${generateRowID()}_name`,
                    current: item,
                    characterid: character.id
                });
            });
        });

        // Add appearance as a single attribute
        createObj("attribute", {
            name: "appearance",
            current: data.appearance,
            characterid: character.id
        });

        // Add background and personality traits
        createObj("attribute", {
            name: "background",
            current: data.background,
            characterid: character.id
        });

        createObj("attribute", {
            name: "personality_traits",
            current: data.personality_traits.join(", "),
            characterid: character.id
        });
    }

    // Helper function to generate a unique row ID for repeating sections
    function generateRowID() {
        return Math.random().toString(36).substring(2, 10);
    }

    function createActionsAbility(character, actions) {
        actions.forEach(action => {
            createObj("attribute", {
                name: `repeating_npcaction_${generateRowID()}_name`,
                current: action.name,
                characterid: character.id
            });
            createObj("attribute", {
                name: `repeating_npcaction_${generateRowID()}_description`,
                current: action.description,
                characterid: character.id
            });
        });
    }

    function createBackgroundAbility(character, data) {
        let backgroundText = `Background: ${data.background}\n\n`;
        backgroundText += `Personality Traits: ${data.personality_traits}\n\n`;

        createObj("ability", {
            name: "Background & Personality",
            description: backgroundText,
            characterid: character.id
        });
    }

    function registerEventHandlers() {
        on('chat:message', handleInput);
    }

    return {
        registerEventHandlers: registerEventHandlers
    };
}());

on('ready', function() {
    'use strict';
    createNPC.registerEventHandlers();
    log('NPC Creation Script loaded');
});

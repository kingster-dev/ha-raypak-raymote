# ha-raypak-raymote
A Home Assistant integration capable of driving a RayPak Avia Pool/Spa Heater via Web API Calls

Completely beta, just getting started!!!
Home Assistant - Blynk API Integration

This is a custom integration for Home Assistant that allows you to connect and control devices on the Blynk IoT Platform.

It allows you to add Blynk sensors and switches to Home Assistant, enabling you to read sensor data and control digital pins from your dashboard and automations.
Key Features

    Simple Setup: Configure entirely through the Home Assistant UI.

    Sensors: Monitor any virtual or digital pin as a sensor entity.

    Switches: Control any digital pin as a switch entity.

    Options Flow: Add and remove pins dynamically from the integration's "Configure" menu without restarting.

    Cloud & Local Server: Works with the official Blynk cloud or your own local Blynk server.

Installation (HACS)

The easiest way to install this integration is with the Home Assistant Community Store (HACS).

    Open HACS.

    Go to Integrations > Click the 3-dots in the top right > Custom repositories.

    Add the URL to this repository in the Repository field.

    Select Integration as the category.

    Click "ADD".

    You will now find the "Blynk API" integration in the HACS store. Click "INSTALL".

    Restart Home Assistant.

Configuration

    Navigate to Settings -> Devices & Services.

    Click "+ ADD INTEGRATION" and search for "Blynk API".

    Enter your Blynk Auth Token and Server URL.

        The default server is https://blynk.cloud. If you use a local server, change it accordingly (e.g., http://192.168.1.100).

    After the integration is added, click "CONFIGURE" on the integration card.

    Use the "Manage Sensors" and "Manage Switches" menus to add the pins you want to control or monitor.

Example Lovelace Card

You can use a simple Entities card to display your new Blynk entities on a dashboard. First, find your entity IDs by going to Settings > Devices & Services > Entities. They will look similar to the examples below.

type: entities
title: Blynk Controls
entities:
  - entity: sensor.blynk_living_room_temperature
  - entity: switch.blynk_main_light

Contributions

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

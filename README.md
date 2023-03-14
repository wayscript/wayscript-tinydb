# TinyDB API Lair template

A simple [TinyDB](https://tinydb.readthedocs.io/en/latest/) API Lair template that can be used to provision databases quickly.

## Setup

To start using this API -

1. Create a new WayScript Lair from this template
2. Deploy lair by running the pre-configured deploy trigger

You can checkout the available API endpoints by visiting the [default endpoint](https://docs.wayscript.com/platform/lairs/endpoints) of your deployed Lair. 

### Persist database
The service stores the database in your lair root in `db.json`. In WayScript, you can deploy to a `dev` or a `prod` environment. Changes to the lair storage made in `dev` would be saved to the lair while changes made in `prod` are not saved. Therefore, to persist the database across invocations, you should run the service only in the `dev` environment. 
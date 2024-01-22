# CloudView

A consolidated webview of cloud-synced data. Safari Cloud Tabs, Firefox Sync Tabs, Tot Dots (becuse [tot.rocks](https://tot.rocks)).

## Setup/Installation

### Firefox Sync Tabs

To display firefox tabs, first install the [firefox-sync-client](https://github.com/Mikescher/firefox-sync-client) as instructed (anywhere is fine). And then login:

```bash
ffsclient login {username} {password}
```

You can verify that you're logged in successfully and your tabs are accessible by running:

```bash
ffsclient tabs list
```

Then, in the [config.toml](./config.toml) update the `firefox` section with the path to the executable file:

```toml
[firefox]
enabled = true
ffsclient = "/Path/to/ffsclient"
```

### Safari Cloud Tabs

Safari tabs are read from the `CloudTabs.db` file stored on disk. _Typically_ this will be stored at `~/Library/Containers/com.apple.Safari/Data/Library/Safari/CloudTabs.db`. However you should verify this location on your system. You may need to allow Full Disk Access for python and/or the terminal for this to work.

Update [config.toml](./config.toml) with the path to the `CloudTabs.db`` file:

```toml
[safari]
enabled = true
cloudtabs = "~/Library/Containers/com.apple.Safari/Data/Library/Safari/CloudTabs.db"
```

### Tot Dots

A shortcut is used to query Tot for its data and return it in JSON format. You will need [Tot](https://tot.rocks) installed (and probably running).

Additinally, add the [TotToJson](https://www.icloud.com/shortcuts/885a89555e5d421aaacbfe850f11b7d0) shortcut. If you rename the shortcut, be sure to update the name in the [config.toml](./config.toml).
# NetBox v4.2

## v4.2.5 (2025-03-06)

### Enhancements

* [#17357](https://github.com/netbox-community/netbox/issues/17357) - Use VirtualChassis name as fallback for unnamed devices
* [#17542](https://github.com/netbox-community/netbox/issues/17542) - Add contact assignments to VPN tunnels
* [#17944](https://github.com/netbox-community/netbox/issues/17944) - Allow script inputs to be filtered on ObjectVar and MultiObjectVar selections
* [#18024](https://github.com/netbox-community/netbox/issues/18024) - Add permalink URL pattern to match a custom script by module and class name
* [#18095](https://github.com/netbox-community/netbox/issues/18095) - Ensure contacts are shown on children of objects with contacts
* [#18141](https://github.com/netbox-community/netbox/issues/18141) - Support "Quick Add" for plugins
* [#18403](https://github.com/netbox-community/netbox/issues/18403) - Improve performance of job list views
* [#18693](https://github.com/netbox-community/netbox/issues/18693) - Support setting VLAN translation on bulk edit of interfaces
* [#18772](https://github.com/netbox-community/netbox/issues/18772) - Add "type" filter for virtual circuits
* [#18774](https://github.com/netbox-community/netbox/issues/18774) - Add tooltip preview of tag descriptions when hovering over tags

### Bug Fixes

* [#15016](https://github.com/netbox-community/netbox/issues/15016) - Prevent AssertionError when adding multiple devices "mid-span" in a cable trace
* [#15924](https://github.com/netbox-community/netbox/issues/15924) - Prevent setting tagged VLANs on interfaces with mode: tagged-all
* [#17488](https://github.com/netbox-community/netbox/issues/17488) - Ensure VLANGroup.vid_ranges shows up in API results
* [#17709](https://github.com/netbox-community/netbox/issues/17709) - Allow primary key for nested models in OpenAPI request schemas
* [#17796](https://github.com/netbox-community/netbox/issues/17796) - Fix IndexError on "Create & Add Another" operation on custom field choices
* [#18605](https://github.com/netbox-community/netbox/issues/18605) - Limit VLAN selection dropdown to choices appropriate to site
* [#18722](https://github.com/netbox-community/netbox/issues/18722) - Improve UI feedback on failed script execution
* [#18729](https://github.com/netbox-community/netbox/issues/18729) - Fix unpredictable ordering on querysets with annotations/groupings
* [#18753](https://github.com/netbox-community/netbox/issues/18753) - Prevent webhooks from being triggered on a script dry-run
* [#18758](https://github.com/netbox-community/netbox/issues/18758) - Fix FieldError when sorting by account count field in providers list
* [#18768](https://github.com/netbox-community/netbox/issues/18768) - Fix removing a secondary MAC address from an interface

---

## v4.2.4 (2025-02-21)

### Enhancements

* [#17309](https://github.com/netbox-community/netbox/issues/17309) - Omit empty counts in related object tables
* [#18277](https://github.com/netbox-community/netbox/issues/18277) - Improve multi-table inheritance in serialization of change-logged models
* [#18286](https://github.com/netbox-community/netbox/issues/18286) - Add more job duration choices
* [#18357](https://github.com/netbox-community/netbox/issues/18357) - Display author name in plugin list for locally installed plugins
* [#18408](https://github.com/netbox-community/netbox/issues/18408) - Add Paused status for virtual machines
* [#18584](https://github.com/netbox-community/netbox/issues/18584) - Add rack type column to manufacturer list

### Bug Fixes

* [#17436](https://github.com/netbox-community/netbox/issues/17436) - Fix {module} replacement in module bays
* [#18013](https://github.com/netbox-community/netbox/issues/18013) - Limit object type to selected object in change log filter
* [#18241](https://github.com/netbox-community/netbox/issues/18241) - Default logging level of custom scripts changed to INFO
* [#18247](https://github.com/netbox-community/netbox/issues/18247) - Fix visibility of disabled cable paths in dark mode
* [#18480](https://github.com/netbox-community/netbox/issues/18480) - Clean data passed to script in runscript command
* [#18555](https://github.com/netbox-community/netbox/issues/18555) - Add default get_absolute_url method to plugin models
* [#18585](https://github.com/netbox-community/netbox/issues/18585) - Fix filtering circuits by location
* [#18593](https://github.com/netbox-community/netbox/issues/18593) - Fix "Create & Add Another" IP Address workflow
* [#18594](https://github.com/netbox-community/netbox/issues/18594) - Enable sorting by ASN count on site and provider lists
* [#18619](https://github.com/netbox-community/netbox/issues/18619) - Ensure shift-click selection selects only visible list items
* [#18674](https://github.com/netbox-community/netbox/issues/18674) - Preserve form values when selecting speed on circuit termination

---

## v4.2.3 (2025-02-04)

### Enhancements

* [#18518](https://github.com/netbox-community/netbox/issues/18518) - Add a "hostname" `<meta>` tag to the page header

### Bug Fixes

* [#18497](https://github.com/netbox-community/netbox/issues/18497) - Fix unhandled `FieldDoesNotExist` exception when search results include virtual circuit
* [#18433](https://github.com/netbox-community/netbox/issues/18433) - Fix MAC address not shown as "primary for interface" in MAC address detail view
* [#18154](https://github.com/netbox-community/netbox/issues/18154) - Allow anonymous users to change default table preferences
* [#18515](https://github.com/netbox-community/netbox/issues/18515) - Fix Django `collectstatic` management command in debug mode with Redis not running
* [#18456](https://github.com/netbox-community/netbox/issues/18456) - Avoid duplicate MAC Address column in interface tables
* [#18447](https://github.com/netbox-community/netbox/issues/18447) - Fix `FieldError` exception when sorting interface tables on MAC Address columns 
* [#18438](https://github.com/netbox-community/netbox/issues/18438) - Improve performance in IPAM migration `0072_prefix_cached_relations` when upgrading from v4.1 or earlier
* [#18436](https://github.com/netbox-community/netbox/issues/18436) - Reset primary MAC address when unassigning MAC address from interface
* [#18181](https://github.com/netbox-community/netbox/issues/18181) - Fix "Create & Add Another" workflow when adding IP addresses to interfaces

---

## v4.2.2 (2025-01-17)

### Bug Fixes

* [#18336](https://github.com/netbox-community/netbox/issues/18336) - Validate new rack height against installed devices when changing a rack's type
* [#18350](https://github.com/netbox-community/netbox/issues/18350) - Fix `FieldDoesNotExist` exception when global search results include a circuit termination
* [#18353](https://github.com/netbox-community/netbox/issues/18353) - Disable fetching of plugin catalog data when `ISOLATED_DEPLOYMENT` is enabled
* [#18362](https://github.com/netbox-community/netbox/issues/18362) - Avoid transmitting census data on every worker restart
* [#18363](https://github.com/netbox-community/netbox/issues/18363) - Fix support for assigning a MAC address to an interface via the REST API
* [#18368](https://github.com/netbox-community/netbox/issues/18368) - Restore missing attributes from REST API serializer for MAC addresses (`tags`, `created`, `last_updated`, and custom fields)
* [#18369](https://github.com/netbox-community/netbox/issues/18369) - Fix `TypeError` exception when rendering the system configuration view with one or more custom classes defined under `PROTECTION_RULES`
* [#18373](https://github.com/netbox-community/netbox/issues/18373) - Fix `AttributeError` exception when attempting to assign host devices to a cluster
* [#18376](https://github.com/netbox-community/netbox/issues/18376) - Fix the display of tagged VLANs in interfaces list for Q-in-Q interfaces
* [#18379](https://github.com/netbox-community/netbox/issues/18379) - Ensure RSS feed dashboard widget content is sanitized
* [#18392](https://github.com/netbox-community/netbox/issues/18392) - Virtual machines should not inherit config contexts assigned to locations
* [#18400](https://github.com/netbox-community/netbox/issues/18400) - Fix support for `STORAGE_BACKEND` configuration parameter
* [#18406](https://github.com/netbox-community/netbox/issues/18406) - Scope column headers in object lists should not be orderable

---

## v4.2.1 (2025-01-08)

### Bug Fixes

* [#18282](https://github.com/netbox-community/netbox/issues/18282) - Fix ordering of prefixes list by assigned VLAN
* [#18314](https://github.com/netbox-community/netbox/issues/18314) - Fix KeyError exception when rendering pre-saved dashboard (`requires_internet` missing)
* [#18316](https://github.com/netbox-community/netbox/issues/18316) - Fix AttributeError exception when global search results include prefixes and/or clusters
* [#18318](https://github.com/netbox-community/netbox/issues/18318) - Correct navigation breadcrumbs for module type UI view
* [#18324](https://github.com/netbox-community/netbox/issues/18324) - Correct filtering for certain related object listings
* [#18329](https://github.com/netbox-community/netbox/issues/18329) - Address upstream bug in GraphQL API where only one primary IP address is returned within a device/VM list

---

## v4.2.0 (2025-01-06)

### Breaking Changes

* Support for the Django admin UI has been completely removed. (The Django admin UI was disabled by default in NetBox v4.0.)
* This release drops support for PostgreSQL 12. PostgreSQL 13 or later is required to run this release.
* NetBox has adopted collation-based natural ordering for many models. This may alter the order in which some objects are listed by default.
* Automatic redirects from pre-v4.1 UI views for virtual disks have been removed.
* The `site` and `provider_network` foreign key fields on `circuits.CircuitTermination` have been replaced by the `termination` generic foreign key.
* The `site` foreign key field on `ipam.Prefix` has been replaced by the `scope` generic foreign key.
* The `site` foreign key field on `virtualization.Cluster` has been replaced by the `scope` generic foreign key.
* The `circuit` foreign key field on `circuits.CircuitGroupAssignment` has been replaced by the `member` generic foreign key.
* Obsolete nested REST API serializers have been removed. These were deprecated in NetBox v4.1 under [#17143](https://github.com/netbox-community/netbox/issues/17143).

### New Features

#### Assign Multiple MAC Addresses per Interface ([#4867](https://github.com/netbox-community/netbox/issues/4867))

MAC addresses are now managed as independent objects, rather than attributes on device and VM interfaces. NetBox now supports the assignment of multiple MAC addresses per interface, and allows a primary MAC address to be designated for each.

#### Quick Add UI Widget ([#5858](https://github.com/netbox-community/netbox/issues/5858))

A new UI widget has been introduced to enable conveniently creating new related objects while creating or editing an object. For instance, it is now possible to create and assign a new device role when creating or editing a device from within the device form.

#### VLAN Translation ([#7336](https://github.com/netbox-community/netbox/issues/7336))

User can now define policies which track the translation of VLAN IDs on IEEE 802.1Q-encapsulated interfaces. Translation policies can be reused across multiple interfaces.

#### Virtual Circuits ([#13086](https://github.com/netbox-community/netbox/issues/13086))

New models have been introduced to support the documentation of virtual circuits as an extension to the physical circuit modeling already supported. This enables users to accurately reflect point-to-point or multipoint virtual circuits atop infrastructure comprising physical circuits and cables.

#### Q-in-Q Encapsulation ([#13428](https://github.com/netbox-community/netbox/issues/13428))

NetBox now supports the designation of customer VLANs (CVLANs) and service VLANs (SVLANs) to support IEEE 802.1ad/Q-in-Q encapsulation. Each interface can now have it mode designated "Q-in-Q" and be assigned an SVLAN.

### Enhancements

* [#6414](https://github.com/netbox-community/netbox/issues/6414) - Prefixes can now be scoped by region, site group, site, or location
* [#7699](https://github.com/netbox-community/netbox/issues/7699) - Virtualization clusters can now be scoped by region, site group, site, or location
* [#9604](https://github.com/netbox-community/netbox/issues/9604) - The scope of a circuit termination now include a region, site group, site, location, or provider network
* [#10711](https://github.com/netbox-community/netbox/issues/10711) - Wireless LANs can now be scoped by region, site group, site, or location
* [#11279](https://github.com/netbox-community/netbox/issues/11279) - Improved the use of natural ordering for various models throughout the application
* [#12596](https://github.com/netbox-community/netbox/issues/12596) - Extended the virtualization clusters REST API endpoint to report on allocated VM resources
* [#16547](https://github.com/netbox-community/netbox/issues/16547) - Add a geographic distance field for circuits
* [#16783](https://github.com/netbox-community/netbox/issues/16783) - Add an operational status field for inventory items
* [#17195](https://github.com/netbox-community/netbox/issues/17195) - Add a color field for power outlets

### Plugins

* [#15093](https://github.com/netbox-community/netbox/issues/15093) - Introduced the `events_pipeline` configuration parameter, which allows plugins to hook into NetBox event processing
* [#16546](https://github.com/netbox-community/netbox/issues/16546) - NetBoxModel now provides a default `get_absolute_url()` method
* [#16971](https://github.com/netbox-community/netbox/issues/16971) - Plugins can now easily register system jobs to perform background tasks
* [#17029](https://github.com/netbox-community/netbox/issues/17029) - Registering a `PluginTemplateExtension` subclass for a single model has been deprecated (replace `model` with `models`)
* [#18023](https://github.com/netbox-community/netbox/issues/18023) - Extend `register_model_view()` to handle list views

### Other Changes

* [#16136](https://github.com/netbox-community/netbox/issues/16136) - Removed support for the Django admin UI
* [#17165](https://github.com/netbox-community/netbox/issues/17165) - All obsolete nested REST API serializers have been removed
* [#17472](https://github.com/netbox-community/netbox/issues/17472) - The legacy staged changes API has been deprecated, and will be removed in Netbox v4.3
* [#17476](https://github.com/netbox-community/netbox/issues/17476) - Upgrade to Django 5.1
* [#17752](https://github.com/netbox-community/netbox/issues/17752) - Bulk object import URL paths have been renamed from `*_import` to `*_bulk_import`
* [#17761](https://github.com/netbox-community/netbox/issues/17761) - Optional choice fields now store empty values as null (rather than empty strings) in the database
* [#18093](https://github.com/netbox-community/netbox/issues/18093) - Redirects for pre-v4.1 virtual disk UI views have been removed

### REST API Changes

* Added the following endpoints:
    * `/api/circuits/virtual-circuits/`
    * `/api/circuits/virtual-circuit-terminations/`
    * `/api/dcim/mac-addresses/`
    * `/api/ipam/vlan-translation-policies/`
    * `/api/ipam/vlan-translation-rules/`
* circuits.Circuit
    * Added the optional `distance` and `distance_unit` fields
* circuits.CircuitGroupAssignment
    * Replaced the `circuit` field with `member_type` and `member_id` to support virtual circuit assignment
* circuits.CircuitTermination
    * Removed the `site` & `provider_network` fields
    * Added the `termination_type` & `termination_id` fields to facilitate termination assignment
    * Added the read-only `termination` field
* dcim.Interface
    * The `mac_address` field is now read-only
    * Added the `primary_mac_address` relation to dcim.MACAddress
    * Added the read-only `mac_addresses` list
    * Added the `qinq_svlan` relation to ipam.VLAN
    * Added the `vlan_translation_policy` relation to ipam.VLANTranslationPolicy
    * Added `mode` choice "Q-in-Q"
* dcim.InventoryItem
    * Added the optional `status` choice field
* dcim.Location
    * Added the read-only `prefix_count` field
* dcim.PowerOutlet
    * Added the optional `color` field
* dcim.Region
    * Added the read-only `prefix_count` field
* dcim.SiteGroup
    * Added the read-only `prefix_count` field
* ipam.Prefix
    * Removed the `site` field
    * Added the `scope_type` & `scope_id` fields to facilitate scope assignment
    * Added the read-only `scope` field
* ipam.VLAN
    * Added the optional `qinq_role` selection field
    * Added the `qinq_svlan` recursive relation
* virtualization.Cluster
    * Removed the `site` field
    * Added the `scope_type` & `scope_id` fields to facilitate scope assignment
    * Added the read-only `scope` field
* virtualization.Cluster
    * Added the read-only fields `allocated_vcpus`, `allocated_memory`, and `allocated_disk`
* virtualization.VMInterface
    * The `mac_address` field is now read-only
    * Added the `primary_mac_address` relation to dcim.MACAddress
    * Added the read-only `mac_addresses` list
    * Added the `qinq_svlan` relation to ipam.VLAN
    * Added the `vlan_translation_policy` relation to ipam.VLANTranslationPolicy
    * Added `mode` choice "Q-in-Q"
* wireless.WirelessLAN
    * Added the `scope_type` & `scope_id` fields to support scope assignment
    * Added the read-only `scope` field

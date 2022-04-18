---
title: ODX, OTX, UDS
author: "-"
date: 2017-08-14T04:23:33+00:00
url: /?p=11045
categories:
  - Uncategorized

tags:
  - reprint
---
## ODX, OTX, UDS

<https://blog.softing.com/blog/automotive-electronics/diagnostics-odx-otx-uds-and-other-market-standards/>

Diagnostics – ODX, OTX, UDS and other market standards
  
Posted on 01/07/2015 by Stephan Obermüller
  
Diagnose_Icon_626_251
  
A large number of today's innovations are based on software developments, and vehicles are no exception. Software innovations improve vehicle performance and increase both the safety and sustainability of mobility. The number of ECUs and the associated networking are continually increasing in the process. The associated growing complexity must be mastered over a vehicle's entire lifetime. In addition to actual control functions, diagnostics is increasingly a focal point in development. Although diagnostics was originally only intended for checking that legal emissions standards were being adhered to, it now takes its place before engineering in the entire value chain.

In the past, vehicle manufacturers spent a lot of time and money developing their own proprietary systems for ECU communication, systems that worked with non-compatible formats for data description. This made it virtually impossible for suppliers to use the same software when working with different manufacturers. When no appropriate standards are available, costs are immense and manufacturers can become dependent on specific suppliers. This is why vehicle manufacturers and software suppliers got together to specify and implement a whole range of international standards.

The most significant standards for diagnostics are:
  
– Unified Diagnostic Services (UDS) as a diagnostic protocol compliant with ISO 14229
  
– Communication system (D-Server) compliant with ISO 22900 and 22901

The interfaces of the D-Server are also completely standardized. The data interface defines Open Diagnostic Data Exchange (ODX) as a data model and universal exchange format. Furthermore, the application interface (D-Server API) allows symbolic access to ECU and vehicle information. Using the bus system interface (D-PDU API), it is possible to use different bus protocols and vehicle communication interfaces (VCIs) from various manufacturers.

The Standard Open Test Sequence Exchange (OTX) also makes it possible for users to write diagnostic sequences technically in XML and also enables access to diagnostic functions, flashing and user interaction to name but a few of the advantages. Unlike Java jobs in ODX, sequences can be reused long term once created.

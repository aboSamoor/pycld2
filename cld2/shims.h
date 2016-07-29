#ifndef _SHIMS_H
#define _SHIMS_H
#ifdef _MSC_VER

#if _MSC_VER > 1000
#pragma once
#endif

#define snprintf _snprintf 
#define vsnprintf _vsnprintf 
#define strcasecmp _stricmp 
#define strncasecmp _strnicmp 

#endif
#endif

/*
 * Generated by asn1c-0.9.29 (http://lionet.info/asn1c)
 * From ASN.1 module "Test-Descriptions"
 * 	found in "/home/rieblr/work/car2x/vanetza/vanetza/asn1/test.asn"
 * 	`asn1c -fcompound-names -fincludes-quoted -no-gen-example`
 */

#ifndef	_VanetzaTest_H_
#define	_VanetzaTest_H_


#include "asn_application.h"

/* Including external dependencies */
#include "NativeInteger.h"
#include "NumericString.h"
#include "constr_SEQUENCE.h"

#ifdef __cplusplus
extern "C" {
#endif

/* Dependencies */
typedef enum VanetzaTest__field {
	VanetzaTest__field_magicValue	= 42
} e_VanetzaTest__field;

/* VanetzaTest */
typedef struct VanetzaTest {
	long	 field;
	NumericString_t	 string;
	
	/* Context for parsing across buffer boundaries */
	asn_struct_ctx_t _asn_ctx;
} VanetzaTest_t;

/* Implementation */
extern asn_TYPE_descriptor_t asn_DEF_VanetzaTest;

#ifdef __cplusplus
}
#endif

#endif	/* _VanetzaTest_H_ */
#include "asn_internal.h"

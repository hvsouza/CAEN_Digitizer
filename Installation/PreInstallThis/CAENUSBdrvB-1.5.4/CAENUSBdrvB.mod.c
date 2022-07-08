#include <linux/module.h>
#define INCLUDE_VERMAGIC
#include <linux/build-salt.h>
#include <linux/elfnote-lto.h>
#include <linux/vermagic.h>
#include <linux/compiler.h>

BUILD_SALT;
BUILD_LTO_INFO;

MODULE_INFO(vermagic, VERMAGIC_STRING);
MODULE_INFO(name, KBUILD_MODNAME);

__visible struct module __this_module
__section(".gnu.linkonce.this_module") = {
	.name = KBUILD_MODNAME,
	.init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
	.exit = cleanup_module,
#endif
	.arch = MODULE_ARCH_INIT,
};

#ifdef CONFIG_RETPOLINE
MODULE_INFO(retpoline, "Y");
#endif

static const struct modversion_info ____versions[]
__used __section("__versions") = {
	{ 0x2f1b9ab7, "module_layout" },
	{ 0x7737daab, "usb_deregister" },
	{ 0x93df1b24, "usb_register_driver" },
	{ 0xf0ca6d41, "current_task" },
	{ 0x13c49cc2, "_copy_from_user" },
	{ 0xbc2ca4b9, "usb_control_msg" },
	{ 0x409bcb62, "mutex_unlock" },
	{ 0x2ab7989d, "mutex_lock" },
	{ 0xb8b9f817, "kmalloc_order_trace" },
	{ 0xf6fc4909, "usb_register_dev" },
	{ 0xdcc1a13d, "kmem_cache_alloc_trace" },
	{ 0x5eb946b4, "kmalloc_caches" },
	{ 0x9553396f, "usb_deregister_dev" },
	{ 0x37a0cba, "kfree" },
	{ 0xc959d152, "__stack_chk_fail" },
	{ 0xc5850110, "printk" },
	{ 0x800473f, "__cond_resched" },
	{ 0xf78c6e35, "usb_clear_halt" },
	{ 0x6b10bee1, "_copy_to_user" },
	{ 0x88db9f48, "__check_object_size" },
	{ 0x9cabc106, "usb_bulk_msg" },
	{ 0x977f511b, "__mutex_init" },
	{ 0xd9a5ea54, "__init_waitqueue_head" },
	{ 0xcf2a6966, "up" },
	{ 0x6626afca, "down" },
	{ 0xbdfb6dbb, "__fentry__" },
};

MODULE_INFO(depends, "");

MODULE_ALIAS("usb:v0547p1002d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v21E1p0000d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v21E1p0001d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v21E1p0011d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v21E1p0019d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v21E1p0015d*dc*dsc*dp*ic*isc*ip*in*");

MODULE_INFO(srcversion, "4D79E005A0D0D8D2AB724E6");

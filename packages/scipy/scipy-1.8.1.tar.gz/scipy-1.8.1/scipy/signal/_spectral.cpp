#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/types/ndarray.hpp>
#include <pythonic/include/types/float64.hpp>
#include <pythonic/types/ndarray.hpp>
#include <pythonic/types/float64.hpp>
#include <pythonic/include/builtins/ValueError.hpp>
#include <pythonic/include/builtins/ZeroDivisionError.hpp>
#include <pythonic/include/builtins/getattr.hpp>
#include <pythonic/include/builtins/range.hpp>
#include <pythonic/include/numpy/arctan2.hpp>
#include <pythonic/include/numpy/cos.hpp>
#include <pythonic/include/numpy/empty_like.hpp>
#include <pythonic/include/numpy/sin.hpp>
#include <pythonic/include/numpy/square.hpp>
#include <pythonic/include/operator_/add.hpp>
#include <pythonic/include/operator_/div.hpp>
#include <pythonic/include/operator_/eq.hpp>
#include <pythonic/include/operator_/iadd.hpp>
#include <pythonic/include/operator_/mul.hpp>
#include <pythonic/include/operator_/ne.hpp>
#include <pythonic/include/operator_/sub.hpp>
#include <pythonic/include/types/slice.hpp>
#include <pythonic/include/types/str.hpp>
#include <pythonic/builtins/ValueError.hpp>
#include <pythonic/builtins/ZeroDivisionError.hpp>
#include <pythonic/builtins/getattr.hpp>
#include <pythonic/builtins/range.hpp>
#include <pythonic/numpy/arctan2.hpp>
#include <pythonic/numpy/cos.hpp>
#include <pythonic/numpy/empty_like.hpp>
#include <pythonic/numpy/sin.hpp>
#include <pythonic/numpy/square.hpp>
#include <pythonic/operator_/add.hpp>
#include <pythonic/operator_/div.hpp>
#include <pythonic/operator_/eq.hpp>
#include <pythonic/operator_/iadd.hpp>
#include <pythonic/operator_/mul.hpp>
#include <pythonic/operator_/ne.hpp>
#include <pythonic/operator_/sub.hpp>
#include <pythonic/types/slice.hpp>
#include <pythonic/types/str.hpp>
namespace __pythran__spectral
{
  struct _lombscargle
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::empty_like{})>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type1;
      typedef __type1 __type2;
      typedef decltype(std::declval<__type0>()(std::declval<__type2>())) __type3;
      typedef typename pythonic::assignable<__type3>::type __type4;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type5;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type2>())) __type7;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type7>::type>::type __type8;
      typedef decltype(std::declval<__type5>()(std::declval<__type8>())) __type9;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type9>::type::iterator>::value_type>::type __type10;
      typedef __type10 __type11;
      typedef indexable<__type11> __type12;
      typedef typename __combined<__type4,__type12>::type __type13;
      typedef double __type14;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::square{})>::type>::type __type15;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::cos{})>::type>::type __type16;
      typedef decltype(std::declval<__type2>()[std::declval<__type11>()]) __type19;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::arctan2{})>::type>::type __type20;
      typedef long __type21;
      typedef typename pythonic::assignable<__type14>::type __type22;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type23;
      typedef __type23 __type24;
      typedef decltype(std::declval<__type0>()(std::declval<__type24>())) __type25;
      typedef typename pythonic::assignable<__type25>::type __type26;
      typedef decltype(pythonic::operator_::mul(std::declval<__type19>(), std::declval<__type24>())) __type31;
      typedef decltype(std::declval<__type16>()(std::declval<__type31>())) __type32;
      typedef typename __combined<__type26,__type32>::type __type33;
      typedef __type33 __type34;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type24>())) __type36;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type36>::type>::type __type37;
      typedef decltype(std::declval<__type5>()(std::declval<__type37>())) __type38;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type38>::type::iterator>::value_type>::type __type39;
      typedef __type39 __type40;
      typedef decltype(std::declval<__type34>()[std::declval<__type40>()]) __type41;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::sin{})>::type>::type __type45;
      typedef decltype(std::declval<__type45>()(std::declval<__type31>())) __type51;
      typedef typename __combined<__type26,__type51>::type __type52;
      typedef __type52 __type53;
      typedef decltype(std::declval<__type53>()[std::declval<__type40>()]) __type55;
      typedef decltype(pythonic::operator_::mul(std::declval<__type41>(), std::declval<__type55>())) __type56;
      typedef decltype(pythonic::operator_::add(std::declval<__type22>(), std::declval<__type56>())) __type57;
      typedef typename __combined<__type22,__type57>::type __type58;
      typedef typename __combined<__type58,__type56>::type __type59;
      typedef __type59 __type60;
      typedef decltype(pythonic::operator_::mul(std::declval<__type21>(), std::declval<__type60>())) __type61;
      typedef decltype(std::declval<__type15>()(std::declval<__type41>())) __type65;
      typedef decltype(pythonic::operator_::add(std::declval<__type22>(), std::declval<__type65>())) __type66;
      typedef typename __combined<__type22,__type66>::type __type67;
      typedef typename __combined<__type67,__type65>::type __type68;
      typedef __type68 __type69;
      typedef decltype(std::declval<__type15>()(std::declval<__type55>())) __type73;
      typedef decltype(pythonic::operator_::add(std::declval<__type22>(), std::declval<__type73>())) __type74;
      typedef typename __combined<__type22,__type74>::type __type75;
      typedef typename __combined<__type75,__type73>::type __type76;
      typedef __type76 __type77;
      typedef decltype(pythonic::operator_::sub(std::declval<__type69>(), std::declval<__type77>())) __type78;
      typedef decltype(std::declval<__type20>()(std::declval<__type61>(), std::declval<__type78>())) __type79;
      typedef decltype(pythonic::operator_::mul(std::declval<__type21>(), std::declval<__type19>())) __type83;
      typedef decltype(pythonic::operator_::div(std::declval<__type79>(), std::declval<__type83>())) __type84;
      typedef typename pythonic::assignable<__type84>::type __type85;
      typedef __type85 __type86;
      typedef decltype(pythonic::operator_::mul(std::declval<__type19>(), std::declval<__type86>())) __type87;
      typedef decltype(std::declval<__type16>()(std::declval<__type87>())) __type88;
      typedef typename pythonic::assignable<__type88>::type __type89;
      typedef __type89 __type90;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type91;
      typedef __type91 __type92;
      typedef decltype(std::declval<__type92>()[std::declval<__type40>()]) __type94;
      typedef decltype(pythonic::operator_::mul(std::declval<__type94>(), std::declval<__type41>())) __type98;
      typedef decltype(pythonic::operator_::add(std::declval<__type22>(), std::declval<__type98>())) __type99;
      typedef typename __combined<__type22,__type99>::type __type100;
      typedef typename __combined<__type100,__type98>::type __type101;
      typedef __type101 __type102;
      typedef decltype(pythonic::operator_::mul(std::declval<__type90>(), std::declval<__type102>())) __type103;
      typedef decltype(std::declval<__type45>()(std::declval<__type87>())) __type109;
      typedef typename pythonic::assignable<__type109>::type __type110;
      typedef __type110 __type111;
      typedef decltype(pythonic::operator_::mul(std::declval<__type94>(), std::declval<__type55>())) __type118;
      typedef decltype(pythonic::operator_::add(std::declval<__type22>(), std::declval<__type118>())) __type119;
      typedef typename __combined<__type22,__type119>::type __type120;
      typedef typename __combined<__type120,__type118>::type __type121;
      typedef __type121 __type122;
      typedef decltype(pythonic::operator_::mul(std::declval<__type111>(), std::declval<__type122>())) __type123;
      typedef decltype(pythonic::operator_::add(std::declval<__type103>(), std::declval<__type123>())) __type124;
      typedef decltype(std::declval<__type15>()(std::declval<__type124>())) __type125;
      typedef decltype(std::declval<__type15>()(std::declval<__type90>())) __type127;
      typedef typename pythonic::assignable<__type127>::type __type128;
      typedef __type128 __type129;
      typedef decltype(pythonic::operator_::mul(std::declval<__type129>(), std::declval<__type69>())) __type131;
      typedef decltype(pythonic::operator_::mul(std::declval<__type21>(), std::declval<__type90>())) __type133;
      typedef decltype(pythonic::operator_::mul(std::declval<__type133>(), std::declval<__type111>())) __type135;
      typedef typename pythonic::assignable<__type135>::type __type136;
      typedef __type136 __type137;
      typedef decltype(pythonic::operator_::mul(std::declval<__type137>(), std::declval<__type60>())) __type139;
      typedef decltype(pythonic::operator_::add(std::declval<__type131>(), std::declval<__type139>())) __type140;
      typedef decltype(std::declval<__type15>()(std::declval<__type111>())) __type142;
      typedef typename pythonic::assignable<__type142>::type __type143;
      typedef __type143 __type144;
      typedef decltype(pythonic::operator_::mul(std::declval<__type144>(), std::declval<__type77>())) __type146;
      typedef decltype(pythonic::operator_::add(std::declval<__type140>(), std::declval<__type146>())) __type147;
      typedef decltype(pythonic::operator_::div(std::declval<__type125>(), std::declval<__type147>())) __type148;
      typedef decltype(pythonic::operator_::mul(std::declval<__type90>(), std::declval<__type122>())) __type151;
      typedef decltype(pythonic::operator_::mul(std::declval<__type111>(), std::declval<__type102>())) __type154;
      typedef decltype(pythonic::operator_::sub(std::declval<__type151>(), std::declval<__type154>())) __type155;
      typedef decltype(std::declval<__type15>()(std::declval<__type155>())) __type156;
      typedef decltype(pythonic::operator_::mul(std::declval<__type129>(), std::declval<__type77>())) __type159;
      typedef decltype(pythonic::operator_::sub(std::declval<__type159>(), std::declval<__type139>())) __type163;
      typedef decltype(pythonic::operator_::mul(std::declval<__type144>(), std::declval<__type69>())) __type166;
      typedef decltype(pythonic::operator_::add(std::declval<__type163>(), std::declval<__type166>())) __type167;
      typedef decltype(pythonic::operator_::div(std::declval<__type156>(), std::declval<__type167>())) __type168;
      typedef decltype(pythonic::operator_::add(std::declval<__type148>(), std::declval<__type168>())) __type169;
      typedef decltype(pythonic::operator_::mul(std::declval<__type14>(), std::declval<__type169>())) __type170;
      typedef container<typename std::remove_reference<__type170>::type> __type171;
      typedef typename __combined<__type13,__type171,__type12>::type __type172;
      typedef __type172 __type173;
      typedef typename pythonic::returnable<__type173>::type __type174;
      typedef __type174 result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    inline
    typename type<argument_type0, argument_type1, argument_type2>::result_type operator()(argument_type0&& x, argument_type1&& y, argument_type2&& freqs) const
    ;
  }  ;
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
  inline
  typename _lombscargle::type<argument_type0, argument_type1, argument_type2>::result_type _lombscargle::operator()(argument_type0&& x, argument_type1&& y, argument_type2&& freqs) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::empty_like{})>::type>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type1;
    typedef __type1 __type2;
    typedef decltype(std::declval<__type0>()(std::declval<__type2>())) __type3;
    typedef typename pythonic::assignable<__type3>::type __type4;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type5;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type2>())) __type7;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type7>::type>::type __type8;
    typedef decltype(std::declval<__type5>()(std::declval<__type8>())) __type9;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type9>::type::iterator>::value_type>::type __type10;
    typedef __type10 __type11;
    typedef indexable<__type11> __type12;
    typedef typename __combined<__type4,__type12>::type __type13;
    typedef double __type14;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::square{})>::type>::type __type15;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::cos{})>::type>::type __type16;
    typedef decltype(std::declval<__type2>()[std::declval<__type11>()]) __type19;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::arctan2{})>::type>::type __type20;
    typedef long __type21;
    typedef typename pythonic::assignable<__type14>::type __type22;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type23;
    typedef __type23 __type24;
    typedef decltype(std::declval<__type0>()(std::declval<__type24>())) __type25;
    typedef typename pythonic::assignable<__type25>::type __type26;
    typedef decltype(pythonic::operator_::mul(std::declval<__type19>(), std::declval<__type24>())) __type31;
    typedef decltype(std::declval<__type16>()(std::declval<__type31>())) __type32;
    typedef typename __combined<__type26,__type32>::type __type33;
    typedef __type33 __type34;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type24>())) __type36;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type36>::type>::type __type37;
    typedef decltype(std::declval<__type5>()(std::declval<__type37>())) __type38;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type38>::type::iterator>::value_type>::type __type39;
    typedef __type39 __type40;
    typedef decltype(std::declval<__type34>()[std::declval<__type40>()]) __type41;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::sin{})>::type>::type __type45;
    typedef decltype(std::declval<__type45>()(std::declval<__type31>())) __type51;
    typedef typename __combined<__type26,__type51>::type __type52;
    typedef __type52 __type53;
    typedef decltype(std::declval<__type53>()[std::declval<__type40>()]) __type55;
    typedef decltype(pythonic::operator_::mul(std::declval<__type41>(), std::declval<__type55>())) __type56;
    typedef decltype(pythonic::operator_::add(std::declval<__type22>(), std::declval<__type56>())) __type57;
    typedef typename __combined<__type22,__type57>::type __type58;
    typedef typename __combined<__type58,__type56>::type __type59;
    typedef __type59 __type60;
    typedef decltype(pythonic::operator_::mul(std::declval<__type21>(), std::declval<__type60>())) __type61;
    typedef decltype(std::declval<__type15>()(std::declval<__type41>())) __type65;
    typedef decltype(pythonic::operator_::add(std::declval<__type22>(), std::declval<__type65>())) __type66;
    typedef typename __combined<__type22,__type66>::type __type67;
    typedef typename __combined<__type67,__type65>::type __type68;
    typedef __type68 __type69;
    typedef decltype(std::declval<__type15>()(std::declval<__type55>())) __type73;
    typedef decltype(pythonic::operator_::add(std::declval<__type22>(), std::declval<__type73>())) __type74;
    typedef typename __combined<__type22,__type74>::type __type75;
    typedef typename __combined<__type75,__type73>::type __type76;
    typedef __type76 __type77;
    typedef decltype(pythonic::operator_::sub(std::declval<__type69>(), std::declval<__type77>())) __type78;
    typedef decltype(std::declval<__type20>()(std::declval<__type61>(), std::declval<__type78>())) __type79;
    typedef decltype(pythonic::operator_::mul(std::declval<__type21>(), std::declval<__type19>())) __type83;
    typedef decltype(pythonic::operator_::div(std::declval<__type79>(), std::declval<__type83>())) __type84;
    typedef typename pythonic::assignable<__type84>::type __type85;
    typedef __type85 __type86;
    typedef decltype(pythonic::operator_::mul(std::declval<__type19>(), std::declval<__type86>())) __type87;
    typedef decltype(std::declval<__type16>()(std::declval<__type87>())) __type88;
    typedef typename pythonic::assignable<__type88>::type __type89;
    typedef __type89 __type90;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type91;
    typedef __type91 __type92;
    typedef decltype(std::declval<__type92>()[std::declval<__type40>()]) __type94;
    typedef decltype(pythonic::operator_::mul(std::declval<__type94>(), std::declval<__type41>())) __type98;
    typedef decltype(pythonic::operator_::add(std::declval<__type22>(), std::declval<__type98>())) __type99;
    typedef typename __combined<__type22,__type99>::type __type100;
    typedef typename __combined<__type100,__type98>::type __type101;
    typedef __type101 __type102;
    typedef decltype(pythonic::operator_::mul(std::declval<__type90>(), std::declval<__type102>())) __type103;
    typedef decltype(std::declval<__type45>()(std::declval<__type87>())) __type109;
    typedef typename pythonic::assignable<__type109>::type __type110;
    typedef __type110 __type111;
    typedef decltype(pythonic::operator_::mul(std::declval<__type94>(), std::declval<__type55>())) __type118;
    typedef decltype(pythonic::operator_::add(std::declval<__type22>(), std::declval<__type118>())) __type119;
    typedef typename __combined<__type22,__type119>::type __type120;
    typedef typename __combined<__type120,__type118>::type __type121;
    typedef __type121 __type122;
    typedef decltype(pythonic::operator_::mul(std::declval<__type111>(), std::declval<__type122>())) __type123;
    typedef decltype(pythonic::operator_::add(std::declval<__type103>(), std::declval<__type123>())) __type124;
    typedef decltype(std::declval<__type15>()(std::declval<__type124>())) __type125;
    typedef decltype(std::declval<__type15>()(std::declval<__type90>())) __type127;
    typedef typename pythonic::assignable<__type127>::type __type128;
    typedef __type128 __type129;
    typedef decltype(pythonic::operator_::mul(std::declval<__type129>(), std::declval<__type69>())) __type131;
    typedef decltype(pythonic::operator_::mul(std::declval<__type21>(), std::declval<__type90>())) __type133;
    typedef decltype(pythonic::operator_::mul(std::declval<__type133>(), std::declval<__type111>())) __type135;
    typedef typename pythonic::assignable<__type135>::type __type136;
    typedef __type136 __type137;
    typedef decltype(pythonic::operator_::mul(std::declval<__type137>(), std::declval<__type60>())) __type139;
    typedef decltype(pythonic::operator_::add(std::declval<__type131>(), std::declval<__type139>())) __type140;
    typedef decltype(std::declval<__type15>()(std::declval<__type111>())) __type142;
    typedef typename pythonic::assignable<__type142>::type __type143;
    typedef __type143 __type144;
    typedef decltype(pythonic::operator_::mul(std::declval<__type144>(), std::declval<__type77>())) __type146;
    typedef decltype(pythonic::operator_::add(std::declval<__type140>(), std::declval<__type146>())) __type147;
    typedef decltype(pythonic::operator_::div(std::declval<__type125>(), std::declval<__type147>())) __type148;
    typedef decltype(pythonic::operator_::mul(std::declval<__type90>(), std::declval<__type122>())) __type151;
    typedef decltype(pythonic::operator_::mul(std::declval<__type111>(), std::declval<__type102>())) __type154;
    typedef decltype(pythonic::operator_::sub(std::declval<__type151>(), std::declval<__type154>())) __type155;
    typedef decltype(std::declval<__type15>()(std::declval<__type155>())) __type156;
    typedef decltype(pythonic::operator_::mul(std::declval<__type129>(), std::declval<__type77>())) __type159;
    typedef decltype(pythonic::operator_::sub(std::declval<__type159>(), std::declval<__type139>())) __type163;
    typedef decltype(pythonic::operator_::mul(std::declval<__type144>(), std::declval<__type69>())) __type166;
    typedef decltype(pythonic::operator_::add(std::declval<__type163>(), std::declval<__type166>())) __type167;
    typedef decltype(pythonic::operator_::div(std::declval<__type156>(), std::declval<__type167>())) __type168;
    typedef decltype(pythonic::operator_::add(std::declval<__type148>(), std::declval<__type168>())) __type169;
    typedef decltype(pythonic::operator_::mul(std::declval<__type14>(), std::declval<__type169>())) __type170;
    typedef container<typename std::remove_reference<__type170>::type> __type171;
    typedef typename __combined<__type13,__type171,__type12>::type __type172;
    typedef typename pythonic::assignable<__type172>::type __type173;
    typedef typename pythonic::assignable<__type33>::type __type174;
    typedef typename pythonic::assignable<__type52>::type __type175;
    typedef typename pythonic::assignable<__type101>::type __type176;
    typedef typename pythonic::assignable<__type121>::type __type177;
    typedef typename pythonic::assignable<__type68>::type __type178;
    typedef typename pythonic::assignable<__type76>::type __type179;
    typedef typename pythonic::assignable<__type59>::type __type180;
    if (pythonic::operator_::ne(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, x), pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, y)))
    {
      throw pythonic::builtins::functor::ValueError{}(pythonic::types::str("Input arrays do not have the same size."));
    }
    __type173 pgram = pythonic::numpy::functor::empty_like{}(freqs);
    __type174 c = pythonic::numpy::functor::empty_like{}(x);
    __type175 s = pythonic::numpy::functor::empty_like{}(x);
    {
      long  __target139832511447344 = std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, freqs));
      for (long  i=0L; i < __target139832511447344; i += 1L)
      {
        __type176 xc = 0.0;
        __type177 xs = 0.0;
        __type178 cc = 0.0;
        __type179 ss = 0.0;
        __type180 cs = 0.0;
        c[pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None)] = pythonic::numpy::functor::cos{}(pythonic::operator_::mul(freqs[i], x));
        s[pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None)] = pythonic::numpy::functor::sin{}(pythonic::operator_::mul(freqs[i], x));
        {
          long  __target139832508305520 = std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, x));
          for (long  j=0L; j < __target139832508305520; j += 1L)
          {
            xc += pythonic::operator_::mul(y[j], c[j]);
            xs += pythonic::operator_::mul(y[j], s[j]);
            cc += pythonic::numpy::functor::square{}(c[j]);
            ss += pythonic::numpy::functor::square{}(s[j]);
            cs += pythonic::operator_::mul(c[j], s[j]);
          }
        }
        if (pythonic::operator_::eq(freqs[i], 0L))
        {
          throw pythonic::builtins::functor::ZeroDivisionError{}();
        }
        typename pythonic::assignable_noescape<decltype(pythonic::operator_::div(pythonic::numpy::functor::arctan2{}(pythonic::operator_::mul(2L, cs), pythonic::operator_::sub(cc, ss)), pythonic::operator_::mul(2L, freqs[i])))>::type tau = pythonic::operator_::div(pythonic::numpy::functor::arctan2{}(pythonic::operator_::mul(2L, cs), pythonic::operator_::sub(cc, ss)), pythonic::operator_::mul(2L, freqs[i]));
        typename pythonic::assignable_noescape<decltype(pythonic::numpy::functor::cos{}(pythonic::operator_::mul(freqs[i], tau)))>::type c_tau = pythonic::numpy::functor::cos{}(pythonic::operator_::mul(freqs[i], tau));
        typename pythonic::assignable_noescape<decltype(pythonic::numpy::functor::sin{}(pythonic::operator_::mul(freqs[i], tau)))>::type s_tau = pythonic::numpy::functor::sin{}(pythonic::operator_::mul(freqs[i], tau));
        typename pythonic::assignable_noescape<decltype(pythonic::numpy::functor::square{}(c_tau))>::type c_tau2 = pythonic::numpy::functor::square{}(c_tau);
        typename pythonic::assignable_noescape<decltype(pythonic::numpy::functor::square{}(s_tau))>::type s_tau2 = pythonic::numpy::functor::square{}(s_tau);
        typename pythonic::assignable_noescape<decltype(pythonic::operator_::mul(pythonic::operator_::mul(2L, c_tau), s_tau))>::type cs_tau = pythonic::operator_::mul(pythonic::operator_::mul(2L, c_tau), s_tau);
        pgram[i] = pythonic::operator_::mul(0.5, pythonic::operator_::add(pythonic::operator_::div(pythonic::numpy::functor::square{}(pythonic::operator_::add(pythonic::operator_::mul(c_tau, xc), pythonic::operator_::mul(s_tau, xs))), pythonic::operator_::add(pythonic::operator_::add(pythonic::operator_::mul(c_tau2, cc), pythonic::operator_::mul(cs_tau, cs)), pythonic::operator_::mul(s_tau2, ss))), pythonic::operator_::div(pythonic::numpy::functor::square{}(pythonic::operator_::sub(pythonic::operator_::mul(c_tau, xs), pythonic::operator_::mul(s_tau, xc))), pythonic::operator_::add(pythonic::operator_::sub(pythonic::operator_::mul(c_tau2, ss), pythonic::operator_::mul(cs_tau, cs)), pythonic::operator_::mul(s_tau2, cc)))));
      }
    }
    return pgram;
  }
}
#include <pythonic/python/exception_handler.hpp>
#ifdef ENABLE_PYTHON_MODULE
inline
typename __pythran__spectral::_lombscargle::type<pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>>::result_type _lombscargle0(pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& x, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& y, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& freqs) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__spectral::_lombscargle()(x, y, freqs);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}

static PyObject *
__pythran_wrap__lombscargle0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    
    char const* keywords[] = {"x", "y", "freqs",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2]))
        return to_python(_lombscargle0(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2])));
    else {
        return nullptr;
    }
}

            static PyObject *
            __pythran_wrapall__lombscargle(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap__lombscargle0(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "_lombscargle", "\n""    - _lombscargle(float64[:], float64[:], float64[:])", args, kw);
                });
            }


static PyMethodDef Methods[] = {
    {
    "_lombscargle",
    (PyCFunction)__pythran_wrapall__lombscargle,
    METH_VARARGS | METH_KEYWORDS,
    "\n""_lombscargle(x, y, freqs)\n""\n""Supported prototypes:\n""\n""- _lombscargle(float64[:], float64[:], float64[:])\n""\n""Computes the Lomb-Scargle periodogram.\n""\n""Parameters\n""----------\n""x : array_like\n""    Sample times.\n""y : array_like\n""    Measurement values (must be registered so the mean is zero).\n""freqs : array_like\n""    Angular frequencies for output periodogram.\n""\n""Returns\n""-------\n""pgram : array_like\n""    Lomb-Scargle periodogram.\n""\n""Raises\n""------\n""ValueError\n""    If the input arrays `x` and `y` do not have the same shape.\n""\n""See also\n""--------\n""lombscargle\n""\n"""},
    {NULL, NULL, 0, NULL}
};


#if PY_MAJOR_VERSION >= 3
  static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "_spectral",            /* m_name */
    "Tools for spectral analysis of unequally sampled signals.",         /* m_doc */
    -1,                  /* m_size */
    Methods,             /* m_methods */
    NULL,                /* m_reload */
    NULL,                /* m_traverse */
    NULL,                /* m_clear */
    NULL,                /* m_free */
  };
#define PYTHRAN_RETURN return theModule
#define PYTHRAN_MODULE_INIT(s) PyInit_##s
#else
#define PYTHRAN_RETURN return
#define PYTHRAN_MODULE_INIT(s) init##s
#endif
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(_spectral)(void)
#ifndef _WIN32
__attribute__ ((visibility("default")))
#if defined(GNUC) && !defined(__clang__)
__attribute__ ((externally_visible))
#endif
#endif
;
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(_spectral)(void) {
    import_array()
    #if PY_MAJOR_VERSION >= 3
    PyObject* theModule = PyModule_Create(&moduledef);
    #else
    PyObject* theModule = Py_InitModule3("_spectral",
                                         Methods,
                                         "Tools for spectral analysis of unequally sampled signals."
    );
    #endif
    if(! theModule)
        PYTHRAN_RETURN;
    PyObject * theDoc = Py_BuildValue("(sss)",
                                      "0.11.0",
                                      "2022-05-16 07:19:58.354183",
                                      "b56cff7c57981a37e4a502cd99394a47b45590ea94b06fe3923cf38ac2cdffd3");
    if(! theDoc)
        PYTHRAN_RETURN;
    PyModule_AddObject(theModule,
                       "__pythran__",
                       theDoc);


    PYTHRAN_RETURN;
}

#endif
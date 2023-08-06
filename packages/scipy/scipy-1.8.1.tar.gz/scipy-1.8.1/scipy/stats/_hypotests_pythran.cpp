#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/types/float.hpp>
#include <pythonic/include/types/ndarray.hpp>
#include <pythonic/include/types/int.hpp>
#include <pythonic/include/types/int64.hpp>
#include <pythonic/include/types/numpy_texpr.hpp>
#include <pythonic/types/ndarray.hpp>
#include <pythonic/types/numpy_texpr.hpp>
#include <pythonic/types/int64.hpp>
#include <pythonic/types/int.hpp>
#include <pythonic/types/float.hpp>
#include <pythonic/include/builtins/getattr.hpp>
#include <pythonic/include/builtins/int_.hpp>
#include <pythonic/include/builtins/max.hpp>
#include <pythonic/include/builtins/min.hpp>
#include <pythonic/include/builtins/range.hpp>
#include <pythonic/include/builtins/tuple.hpp>
#include <pythonic/include/numpy/ceil.hpp>
#include <pythonic/include/numpy/float64.hpp>
#include <pythonic/include/numpy/floor.hpp>
#include <pythonic/include/numpy/ones.hpp>
#include <pythonic/include/numpy/square.hpp>
#include <pythonic/include/numpy/sum.hpp>
#include <pythonic/include/operator_/add.hpp>
#include <pythonic/include/operator_/div.hpp>
#include <pythonic/include/operator_/eq.hpp>
#include <pythonic/include/operator_/floordiv.hpp>
#include <pythonic/include/operator_/gt.hpp>
#include <pythonic/include/operator_/iadd.hpp>
#include <pythonic/include/operator_/le.hpp>
#include <pythonic/include/operator_/lt.hpp>
#include <pythonic/include/operator_/mul.hpp>
#include <pythonic/include/operator_/sub.hpp>
#include <pythonic/include/types/slice.hpp>
#include <pythonic/include/types/str.hpp>
#include <pythonic/builtins/getattr.hpp>
#include <pythonic/builtins/int_.hpp>
#include <pythonic/builtins/max.hpp>
#include <pythonic/builtins/min.hpp>
#include <pythonic/builtins/range.hpp>
#include <pythonic/builtins/tuple.hpp>
#include <pythonic/numpy/ceil.hpp>
#include <pythonic/numpy/float64.hpp>
#include <pythonic/numpy/floor.hpp>
#include <pythonic/numpy/ones.hpp>
#include <pythonic/numpy/square.hpp>
#include <pythonic/numpy/sum.hpp>
#include <pythonic/operator_/add.hpp>
#include <pythonic/operator_/div.hpp>
#include <pythonic/operator_/eq.hpp>
#include <pythonic/operator_/floordiv.hpp>
#include <pythonic/operator_/gt.hpp>
#include <pythonic/operator_/iadd.hpp>
#include <pythonic/operator_/le.hpp>
#include <pythonic/operator_/lt.hpp>
#include <pythonic/operator_/mul.hpp>
#include <pythonic/operator_/sub.hpp>
#include <pythonic/types/slice.hpp>
#include <pythonic/types/str.hpp>
namespace __pythran__hypotests_pythran
{
  struct _compute_outer_prob_inside_method
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type0;
      typedef __type0 __type1;
      typedef __type1 __type2;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type3;
      typedef __type3 __type4;
      typedef __type4 __type5;
      typedef double __type6;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::ones{})>::type>::type __type7;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::min{})>::type>::type __type8;
      typedef long __type9;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::int_{})>::type>::type __type10;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::ceil{})>::type>::type __type11;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type12;
      typedef __type12 __type13;
      typedef typename pythonic::assignable<__type4>::type __type14;
      typedef typename pythonic::assignable<__type1>::type __type15;
      typedef __type15 __type16;
      typedef __type14 __type17;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type16>(), std::declval<__type17>())) __type18;
      typedef typename pythonic::assignable<__type18>::type __type19;
      typedef __type19 __type20;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type20>::type>::type __type21;
      typedef typename pythonic::assignable<__type21>::type __type22;
      typedef typename __combined<__type14,__type22>::type __type23;
      typedef __type23 __type24;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type25;
      typedef __type25 __type26;
      typedef decltype(pythonic::operator_::functor::floordiv()(std::declval<__type24>(), std::declval<__type26>())) __type27;
      typedef typename pythonic::assignable<__type27>::type __type28;
      typedef __type28 __type29;
      typedef decltype(pythonic::operator_::div(std::declval<__type13>(), std::declval<__type29>())) __type30;
      typedef decltype(std::declval<__type11>()(std::declval<__type30>())) __type31;
      typedef decltype(std::declval<__type10>()(std::declval<__type31>())) __type32;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type20>::type>::type __type33;
      typedef typename pythonic::assignable<__type33>::type __type34;
      typedef typename __combined<__type15,__type34>::type __type35;
      typedef __type35 __type36;
      typedef decltype(pythonic::operator_::add(std::declval<__type36>(), std::declval<__type9>())) __type37;
      typedef decltype(std::declval<__type8>()(std::declval<__type32>(), std::declval<__type37>())) __type38;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type9>(), std::declval<__type38>())) __type39;
      typedef typename pythonic::assignable<__type39>::type __type40;
      typedef std::integral_constant<long,0> __type41;
      typedef __type40 __type42;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type42>::type>::type __type43;
      typedef indexable_container<__type41, typename std::remove_reference<__type43>::type> __type44;
      typedef typename __combined<__type40,__type44>::type __type45;
      typedef __type45 __type46;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type46>::type>::type __type47;
      typedef typename pythonic::assignable<__type47>::type __type48;
      typedef __type48 __type49;
      typedef decltype(pythonic::operator_::mul(std::declval<__type9>(), std::declval<__type49>())) __type50;
      typedef decltype(pythonic::operator_::add(std::declval<__type50>(), std::declval<__type9>())) __type51;
      typedef decltype(std::declval<__type8>()(std::declval<__type51>(), std::declval<__type37>())) __type54;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::float64{})>::type>::type __type55;
      typedef decltype(std::declval<__type7>()(std::declval<__type54>(), std::declval<__type55>())) __type56;
      typedef typename pythonic::assignable<__type56>::type __type57;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type58;
      typedef decltype(pythonic::operator_::functor::floordiv()(std::declval<__type36>(), std::declval<__type26>())) __type61;
      typedef typename pythonic::assignable<__type61>::type __type62;
      typedef __type62 __type63;
      typedef decltype(pythonic::operator_::add(std::declval<__type24>(), std::declval<__type9>())) __type65;
      typedef decltype(std::declval<__type58>()(std::declval<__type9>(), std::declval<__type65>())) __type66;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type66>::type::iterator>::value_type>::type __type67;
      typedef __type67 __type68;
      typedef decltype(pythonic::operator_::mul(std::declval<__type63>(), std::declval<__type68>())) __type69;
      typedef decltype(pythonic::operator_::add(std::declval<__type69>(), std::declval<__type13>())) __type71;
      typedef decltype(pythonic::operator_::div(std::declval<__type71>(), std::declval<__type29>())) __type73;
      typedef decltype(std::declval<__type11>()(std::declval<__type73>())) __type74;
      typedef decltype(std::declval<__type10>()(std::declval<__type74>())) __type75;
      typedef decltype(std::declval<__type8>()(std::declval<__type75>(), std::declval<__type37>())) __type78;
      typedef typename pythonic::assignable<__type78>::type __type79;
      typedef typename __combined<__type48,__type79>::type __type80;
      typedef __type80 __type81;
      typedef typename pythonic::assignable<__type43>::type __type82;
      typedef __type82 __type83;
      typedef decltype(pythonic::operator_::sub(std::declval<__type49>(), std::declval<__type83>())) __type86;
      typedef typename pythonic::assignable<__type86>::type __type87;
      typedef __type87 __type88;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type83>(), std::declval<__type88>())) __type89;
      typedef typename pythonic::assignable<__type89>::type __type90;
      typedef __type90 __type91;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type91>::type>::type __type92;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::max{})>::type>::type __type93;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::floor{})>::type>::type __type94;
      typedef decltype(pythonic::operator_::sub(std::declval<__type69>(), std::declval<__type13>())) __type99;
      typedef decltype(pythonic::operator_::div(std::declval<__type99>(), std::declval<__type29>())) __type101;
      typedef decltype(std::declval<__type94>()(std::declval<__type101>())) __type102;
      typedef decltype(std::declval<__type10>()(std::declval<__type102>())) __type103;
      typedef decltype(pythonic::operator_::add(std::declval<__type103>(), std::declval<__type9>())) __type104;
      typedef typename __combined<__type104,__type9>::type __type105;
      typedef decltype(std::declval<__type93>()(std::declval<__type105>(), std::declval<__type9>())) __type106;
      typedef decltype(std::declval<__type8>()(std::declval<__type106>(), std::declval<__type36>())) __type108;
      typedef typename __combined<__type92,__type108>::type __type109;
      typedef typename pythonic::assignable<__type109>::type __type110;
      typedef typename __combined<__type82,__type110>::type __type111;
      typedef __type111 __type112;
      typedef decltype(pythonic::operator_::sub(std::declval<__type81>(), std::declval<__type112>())) __type113;
      typedef decltype(std::declval<__type58>()(std::declval<__type113>())) __type114;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type114>::type::iterator>::value_type>::type __type115;
      typedef __type115 __type116;
      typedef indexable<__type116> __type117;
      typedef typename __combined<__type57,__type117>::type __type118;
      typedef typename pythonic::assignable<__type6>::type __type119;
      typedef typename __combined<__type57,__type6>::type __type120;
      typedef __type120 __type121;
      typedef decltype(pythonic::operator_::add(std::declval<__type116>(), std::declval<__type112>())) __type124;
      typedef typename pythonic::assignable<__type92>::type __type125;
      typedef __type125 __type126;
      typedef decltype(pythonic::operator_::sub(std::declval<__type124>(), std::declval<__type126>())) __type127;
      typedef decltype(std::declval<__type121>()[std::declval<__type127>()]) __type128;
      typedef decltype(pythonic::operator_::mul(std::declval<__type128>(), std::declval<__type68>())) __type130;
      typedef __type119 __type131;
      typedef typename pythonic::assignable<__type124>::type __type135;
      typedef __type135 __type136;
      typedef decltype(pythonic::operator_::mul(std::declval<__type131>(), std::declval<__type136>())) __type137;
      typedef decltype(pythonic::operator_::add(std::declval<__type130>(), std::declval<__type137>())) __type138;
      typedef decltype(pythonic::operator_::add(std::declval<__type68>(), std::declval<__type136>())) __type141;
      typedef decltype(pythonic::operator_::div(std::declval<__type138>(), std::declval<__type141>())) __type142;
      typedef typename pythonic::assignable<__type142>::type __type143;
      typedef typename __combined<__type119,__type143>::type __type144;
      typedef __type144 __type145;
      typedef container<typename std::remove_reference<__type145>::type> __type146;
      typedef typename __combined<__type118,__type6,__type146,__type117,__type9>::type __type147;
      typedef __type147 __type148;
      typedef decltype(pythonic::operator_::sub(std::declval<__type113>(), std::declval<__type9>())) __type152;
      typedef decltype(std::declval<__type148>()[std::declval<__type152>()]) __type153;
      typedef typename __combined<__type6,__type153>::type __type154;
      typedef typename pythonic::returnable<__type154>::type __type155;
      typedef __type2 __ptype0;
      typedef __type5 __ptype1;
      typedef __type155 result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
    inline
    typename type<argument_type0, argument_type1, argument_type2, argument_type3>::result_type operator()(argument_type0&& m, argument_type1&& n, argument_type2&& g, argument_type3&& h) const
    ;
  }  ;
  struct _a_ij_Aij_Dij2
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
      typedef __type0 __type1;
      typedef __type1 __type2;
      typedef long __type5;
      typedef typename pythonic::assignable<__type5>::type __type6;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type8;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type1>())) __type10;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type10>::type>::type __type11;
      typedef typename pythonic::lazy<__type11>::type __type12;
      typedef __type12 __type13;
      typedef decltype(std::declval<__type8>()(std::declval<__type13>())) __type14;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type14>::type::iterator>::value_type>::type __type15;
      typedef __type15 __type16;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type10>::type>::type __type17;
      typedef typename pythonic::lazy<__type17>::type __type18;
      typedef __type18 __type19;
      typedef decltype(std::declval<__type8>()(std::declval<__type19>())) __type20;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type20>::type::iterator>::value_type>::type __type21;
      typedef __type21 __type22;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type16>(), std::declval<__type22>())) __type23;
      typedef decltype(std::declval<__type1>()[std::declval<__type23>()]) __type24;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::square{})>::type>::type __type25;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::sum{})>::type>::type __type26;
      typedef typename pythonic::assignable<__type1>::type __type27;
      typedef typename __combined<__type27,__type1>::type __type28;
      typedef __type28 __type29;
      typedef pythonic::types::contiguous_slice __type30;
      typedef decltype(std::declval<__type29>()(std::declval<__type30>(), std::declval<__type30>())) __type31;
      typedef decltype(std::declval<__type26>()(std::declval<__type31>())) __type32;
      typedef decltype(pythonic::operator_::add(std::declval<__type32>(), std::declval<__type32>())) __type35;
      typedef typename __combined<__type1,__type1>::type __type36;
      typedef typename pythonic::assignable<__type36>::type __type37;
      typedef __type37 __type38;
      typedef decltype(std::declval<__type38>()(std::declval<__type30>(), std::declval<__type30>())) __type39;
      typedef decltype(std::declval<__type26>()(std::declval<__type39>())) __type40;
      typedef decltype(pythonic::operator_::add(std::declval<__type40>(), std::declval<__type40>())) __type43;
      typedef decltype(pythonic::operator_::sub(std::declval<__type35>(), std::declval<__type43>())) __type44;
      typedef decltype(std::declval<__type25>()(std::declval<__type44>())) __type45;
      typedef decltype(pythonic::operator_::mul(std::declval<__type24>(), std::declval<__type45>())) __type46;
      typedef decltype(pythonic::operator_::add(std::declval<__type6>(), std::declval<__type46>())) __type47;
      typedef typename __combined<__type6,__type47>::type __type48;
      typedef typename __combined<__type48,__type46>::type __type49;
      typedef __type49 __type50;
      typedef typename pythonic::returnable<__type50>::type __type51;
      typedef __type2 __ptype4;
      typedef __type2 __ptype5;
      typedef __type51 result_type;
    }  
    ;
    template <typename argument_type0 >
    inline
    typename type<argument_type0>::result_type operator()(argument_type0&& A) const
    ;
  }  ;
  struct _discordant_pairs
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
      typedef __type0 __type1;
      typedef __type1 __type2;
      typedef long __type3;
      typedef typename pythonic::assignable<__type3>::type __type4;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type6;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type1>())) __type8;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type8>::type>::type __type9;
      typedef typename pythonic::lazy<__type9>::type __type10;
      typedef __type10 __type11;
      typedef decltype(std::declval<__type6>()(std::declval<__type11>())) __type12;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type12>::type::iterator>::value_type>::type __type13;
      typedef __type13 __type14;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type8>::type>::type __type15;
      typedef typename pythonic::lazy<__type15>::type __type16;
      typedef __type16 __type17;
      typedef decltype(std::declval<__type6>()(std::declval<__type17>())) __type18;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type18>::type::iterator>::value_type>::type __type19;
      typedef __type19 __type20;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type14>(), std::declval<__type20>())) __type21;
      typedef decltype(std::declval<__type1>()[std::declval<__type21>()]) __type22;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::sum{})>::type>::type __type23;
      typedef typename pythonic::assignable<__type1>::type __type24;
      typedef __type24 __type25;
      typedef pythonic::types::contiguous_slice __type26;
      typedef decltype(std::declval<__type25>()(std::declval<__type26>(), std::declval<__type26>())) __type27;
      typedef decltype(std::declval<__type23>()(std::declval<__type27>())) __type28;
      typedef decltype(pythonic::operator_::add(std::declval<__type28>(), std::declval<__type28>())) __type31;
      typedef decltype(pythonic::operator_::mul(std::declval<__type22>(), std::declval<__type31>())) __type32;
      typedef decltype(pythonic::operator_::add(std::declval<__type4>(), std::declval<__type32>())) __type33;
      typedef typename __combined<__type4,__type33>::type __type34;
      typedef typename __combined<__type34,__type32>::type __type35;
      typedef __type35 __type36;
      typedef typename pythonic::returnable<__type36>::type __type37;
      typedef __type2 __ptype6;
      typedef __type37 result_type;
    }  
    ;
    template <typename argument_type0 >
    inline
    typename type<argument_type0>::result_type operator()(argument_type0&& A) const
    ;
  }  ;
  struct _concordant_pairs
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
      typedef __type0 __type1;
      typedef __type1 __type2;
      typedef long __type3;
      typedef typename pythonic::assignable<__type3>::type __type4;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type6;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type1>())) __type8;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type8>::type>::type __type9;
      typedef typename pythonic::lazy<__type9>::type __type10;
      typedef __type10 __type11;
      typedef decltype(std::declval<__type6>()(std::declval<__type11>())) __type12;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type12>::type::iterator>::value_type>::type __type13;
      typedef __type13 __type14;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type8>::type>::type __type15;
      typedef typename pythonic::lazy<__type15>::type __type16;
      typedef __type16 __type17;
      typedef decltype(std::declval<__type6>()(std::declval<__type17>())) __type18;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type18>::type::iterator>::value_type>::type __type19;
      typedef __type19 __type20;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type14>(), std::declval<__type20>())) __type21;
      typedef decltype(std::declval<__type1>()[std::declval<__type21>()]) __type22;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::sum{})>::type>::type __type23;
      typedef typename pythonic::assignable<__type1>::type __type24;
      typedef __type24 __type25;
      typedef pythonic::types::contiguous_slice __type26;
      typedef decltype(std::declval<__type25>()(std::declval<__type26>(), std::declval<__type26>())) __type27;
      typedef decltype(std::declval<__type23>()(std::declval<__type27>())) __type28;
      typedef decltype(pythonic::operator_::add(std::declval<__type28>(), std::declval<__type28>())) __type31;
      typedef decltype(pythonic::operator_::mul(std::declval<__type22>(), std::declval<__type31>())) __type32;
      typedef decltype(pythonic::operator_::add(std::declval<__type4>(), std::declval<__type32>())) __type33;
      typedef typename __combined<__type4,__type33>::type __type34;
      typedef typename __combined<__type34,__type32>::type __type35;
      typedef __type35 __type36;
      typedef typename pythonic::returnable<__type36>::type __type37;
      typedef __type2 __ptype7;
      typedef __type37 result_type;
    }  
    ;
    template <typename argument_type0 >
    inline
    typename type<argument_type0>::result_type operator()(argument_type0&& A) const
    ;
  }  ;
  struct _Dij
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::sum{})>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type1;
      typedef __type1 __type2;
      typedef pythonic::types::contiguous_slice __type3;
      typedef decltype(std::declval<__type2>()(std::declval<__type3>(), std::declval<__type3>())) __type4;
      typedef decltype(std::declval<__type0>()(std::declval<__type4>())) __type5;
      typedef decltype(pythonic::operator_::add(std::declval<__type5>(), std::declval<__type5>())) __type9;
      typedef typename pythonic::returnable<__type9>::type __type10;
      typedef __type10 result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    inline
    typename type<argument_type0, argument_type1, argument_type2>::result_type operator()(argument_type0&& A, argument_type1&& i, argument_type2&& j) const
    ;
  }  ;
  struct _Aij
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::sum{})>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type1;
      typedef __type1 __type2;
      typedef pythonic::types::contiguous_slice __type3;
      typedef decltype(std::declval<__type2>()(std::declval<__type3>(), std::declval<__type3>())) __type4;
      typedef decltype(std::declval<__type0>()(std::declval<__type4>())) __type5;
      typedef decltype(pythonic::operator_::add(std::declval<__type5>(), std::declval<__type5>())) __type9;
      typedef typename pythonic::returnable<__type9>::type __type10;
      typedef __type10 result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    inline
    typename type<argument_type0, argument_type1, argument_type2>::result_type operator()(argument_type0&& A, argument_type1&& i, argument_type2&& j) const
    ;
  }  ;
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
  inline
  typename _compute_outer_prob_inside_method::type<argument_type0, argument_type1, argument_type2, argument_type3>::result_type _compute_outer_prob_inside_method::operator()(argument_type0&& m, argument_type1&& n, argument_type2&& g, argument_type3&& h) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type0;
    typedef __type0 __type1;
    typedef typename pythonic::assignable<__type1>::type __type2;
    typedef __type2 __type3;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type4;
    typedef __type4 __type5;
    typedef typename pythonic::assignable<__type5>::type __type6;
    typedef __type6 __type7;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type3>(), std::declval<__type7>())) __type8;
    typedef typename pythonic::assignable<__type8>::type __type9;
    typedef __type9 __type10;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type10>::type>::type __type11;
    typedef typename pythonic::assignable<__type11>::type __type12;
    typedef typename __combined<__type6,__type12>::type __type13;
    typedef typename std::tuple_element<1,typename std::remove_reference<__type10>::type>::type __type14;
    typedef typename pythonic::assignable<__type14>::type __type15;
    typedef typename __combined<__type2,__type15>::type __type16;
    typedef typename pythonic::assignable<__type16>::type __type17;
    typedef typename pythonic::assignable<__type13>::type __type18;
    typedef long __type19;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::min{})>::type>::type __type20;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::int_{})>::type>::type __type21;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::ceil{})>::type>::type __type22;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type23;
    typedef __type23 __type24;
    typedef __type13 __type25;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type26;
    typedef __type26 __type27;
    typedef decltype(pythonic::operator_::functor::floordiv()(std::declval<__type25>(), std::declval<__type27>())) __type28;
    typedef typename pythonic::assignable<__type28>::type __type29;
    typedef __type29 __type30;
    typedef decltype(pythonic::operator_::div(std::declval<__type24>(), std::declval<__type30>())) __type31;
    typedef decltype(std::declval<__type22>()(std::declval<__type31>())) __type32;
    typedef decltype(std::declval<__type21>()(std::declval<__type32>())) __type33;
    typedef __type16 __type34;
    typedef decltype(pythonic::operator_::add(std::declval<__type34>(), std::declval<__type19>())) __type35;
    typedef decltype(std::declval<__type20>()(std::declval<__type33>(), std::declval<__type35>())) __type36;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type19>(), std::declval<__type36>())) __type37;
    typedef typename pythonic::assignable<__type37>::type __type38;
    typedef std::integral_constant<long,0> __type39;
    typedef __type38 __type40;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type40>::type>::type __type41;
    typedef indexable_container<__type39, typename std::remove_reference<__type41>::type> __type42;
    typedef std::integral_constant<long,1> __type43;
    typedef typename __combined<__type38,__type42>::type __type44;
    typedef __type44 __type45;
    typedef typename std::tuple_element<1,typename std::remove_reference<__type45>::type>::type __type46;
    typedef indexable_container<__type43, typename std::remove_reference<__type46>::type> __type47;
    typedef typename __combined<__type38,__type42,__type47>::type __type48;
    typedef typename pythonic::assignable<__type48>::type __type49;
    typedef typename pythonic::assignable<__type41>::type __type50;
    typedef __type50 __type51;
    typedef typename pythonic::assignable<__type46>::type __type52;
    typedef decltype(pythonic::operator_::functor::floordiv()(std::declval<__type34>(), std::declval<__type27>())) __type55;
    typedef typename pythonic::assignable<__type55>::type __type56;
    typedef __type56 __type57;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type58;
    typedef decltype(pythonic::operator_::add(std::declval<__type25>(), std::declval<__type19>())) __type60;
    typedef decltype(std::declval<__type58>()(std::declval<__type19>(), std::declval<__type60>())) __type61;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type61>::type::iterator>::value_type>::type __type62;
    typedef __type62 __type63;
    typedef decltype(pythonic::operator_::mul(std::declval<__type57>(), std::declval<__type63>())) __type64;
    typedef decltype(pythonic::operator_::add(std::declval<__type64>(), std::declval<__type24>())) __type66;
    typedef decltype(pythonic::operator_::div(std::declval<__type66>(), std::declval<__type30>())) __type68;
    typedef decltype(std::declval<__type22>()(std::declval<__type68>())) __type69;
    typedef decltype(std::declval<__type21>()(std::declval<__type69>())) __type70;
    typedef decltype(std::declval<__type20>()(std::declval<__type70>(), std::declval<__type35>())) __type73;
    typedef typename pythonic::assignable<__type73>::type __type74;
    typedef typename __combined<__type52,__type74>::type __type75;
    typedef __type75 __type76;
    typedef decltype(pythonic::operator_::sub(std::declval<__type76>(), std::declval<__type51>())) __type78;
    typedef typename pythonic::assignable<__type78>::type __type79;
    typedef __type79 __type80;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type51>(), std::declval<__type80>())) __type81;
    typedef typename pythonic::assignable<__type81>::type __type82;
    typedef __type82 __type83;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type83>::type>::type __type84;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::max{})>::type>::type __type85;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::floor{})>::type>::type __type86;
    typedef decltype(pythonic::operator_::sub(std::declval<__type64>(), std::declval<__type24>())) __type91;
    typedef decltype(pythonic::operator_::div(std::declval<__type91>(), std::declval<__type30>())) __type93;
    typedef decltype(std::declval<__type86>()(std::declval<__type93>())) __type94;
    typedef decltype(std::declval<__type21>()(std::declval<__type94>())) __type95;
    typedef decltype(pythonic::operator_::add(std::declval<__type95>(), std::declval<__type19>())) __type96;
    typedef typename __combined<__type96,__type19>::type __type97;
    typedef decltype(std::declval<__type85>()(std::declval<__type97>(), std::declval<__type19>())) __type98;
    typedef decltype(std::declval<__type20>()(std::declval<__type98>(), std::declval<__type34>())) __type100;
    typedef typename __combined<__type84,__type100>::type __type101;
    typedef typename pythonic::assignable<__type101>::type __type102;
    typedef typename __combined<__type50,__type102>::type __type103;
    typedef __type103 __type105;
    typedef decltype(pythonic::operator_::sub(std::declval<__type76>(), std::declval<__type105>())) __type106;
    typedef typename pythonic::assignable<__type106>::type __type107;
    typedef typename __combined<__type79,__type107>::type __type108;
    typedef typename pythonic::assignable<__type103>::type __type109;
    typedef typename pythonic::assignable<__type75>::type __type110;
    typedef typename pythonic::assignable<__type108>::type __type111;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::ones{})>::type>::type __type112;
    typedef decltype(pythonic::operator_::mul(std::declval<__type19>(), std::declval<__type76>())) __type114;
    typedef decltype(pythonic::operator_::add(std::declval<__type114>(), std::declval<__type19>())) __type115;
    typedef decltype(std::declval<__type20>()(std::declval<__type115>(), std::declval<__type35>())) __type118;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::float64{})>::type>::type __type119;
    typedef decltype(std::declval<__type112>()(std::declval<__type118>(), std::declval<__type119>())) __type120;
    typedef typename pythonic::assignable<__type120>::type __type121;
    typedef decltype(std::declval<__type58>()(std::declval<__type106>())) __type125;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type125>::type::iterator>::value_type>::type __type126;
    typedef __type126 __type127;
    typedef indexable<__type127> __type128;
    typedef typename __combined<__type121,__type128>::type __type129;
    typedef double __type130;
    typedef typename pythonic::assignable<__type130>::type __type131;
    typedef typename __combined<__type121,__type130>::type __type132;
    typedef __type132 __type133;
    typedef decltype(pythonic::operator_::add(std::declval<__type127>(), std::declval<__type105>())) __type136;
    typedef typename pythonic::assignable<__type84>::type __type137;
    typedef __type137 __type138;
    typedef decltype(pythonic::operator_::sub(std::declval<__type136>(), std::declval<__type138>())) __type139;
    typedef decltype(std::declval<__type133>()[std::declval<__type139>()]) __type140;
    typedef decltype(pythonic::operator_::mul(std::declval<__type140>(), std::declval<__type63>())) __type142;
    typedef __type131 __type143;
    typedef typename pythonic::assignable<__type136>::type __type147;
    typedef __type147 __type148;
    typedef decltype(pythonic::operator_::mul(std::declval<__type143>(), std::declval<__type148>())) __type149;
    typedef decltype(pythonic::operator_::add(std::declval<__type142>(), std::declval<__type149>())) __type150;
    typedef decltype(pythonic::operator_::add(std::declval<__type63>(), std::declval<__type148>())) __type153;
    typedef decltype(pythonic::operator_::div(std::declval<__type150>(), std::declval<__type153>())) __type154;
    typedef typename pythonic::assignable<__type154>::type __type155;
    typedef typename __combined<__type131,__type155>::type __type156;
    typedef __type156 __type157;
    typedef container<typename std::remove_reference<__type157>::type> __type158;
    typedef typename __combined<__type129,__type130,__type158,__type128,__type19>::type __type159;
    typedef typename pythonic::assignable<__type159>::type __type160;
    typedef typename pythonic::assignable<__type156>::type __type161;
    __type17 n_ = n;
    __type18 m_ = m;
    if (pythonic::operator_::lt(m_, n_))
    {
      typename pythonic::assignable_noescape<decltype(pythonic::types::make_tuple(n_, m_))>::type __tuple0 = pythonic::types::make_tuple(n_, m_);
      m_ = std::get<0>(__tuple0);
      n_ = std::get<1>(__tuple0);
    }
    typename pythonic::assignable_noescape<decltype(pythonic::operator_::functor::floordiv()(m_, g))>::type mg = pythonic::operator_::functor::floordiv()(m_, g);
    typename pythonic::assignable_noescape<decltype(pythonic::operator_::functor::floordiv()(n_, g))>::type ng = pythonic::operator_::functor::floordiv()(n_, g);
    __type49 __tuple1 = pythonic::types::make_tuple(0L, pythonic::builtins::functor::min{}(pythonic::builtins::functor::int_{}(pythonic::numpy::functor::ceil{}(pythonic::operator_::div(h, mg))), pythonic::operator_::add(n_, 1L)));
    __type109 minj = std::get<0>(__tuple1);
    __type110 maxj = std::get<1>(__tuple1);
    __type111 curlen = pythonic::operator_::sub(maxj, minj);
    __type160 A = pythonic::numpy::functor::ones{}(pythonic::builtins::functor::min{}(pythonic::operator_::add(pythonic::operator_::mul(2L, maxj), 2L), pythonic::operator_::add(n_, 1L)), pythonic::numpy::functor::float64{});
    A[pythonic::types::contiguous_slice(minj,maxj)] = 0.0;
    {
      long  __target139832507546016 = pythonic::operator_::add(m_, 1L);
      for (long  i=1L; i < __target139832507546016; i += 1L)
      {
        typename pythonic::assignable_noescape<decltype(pythonic::types::make_tuple(minj, curlen))>::type __tuple2 = pythonic::types::make_tuple(minj, curlen);
        typename pythonic::assignable_noescape<decltype(std::get<0>(__tuple2))>::type lastminj = std::get<0>(__tuple2);
        minj = pythonic::builtins::functor::min{}(pythonic::builtins::functor::max{}(pythonic::operator_::add(pythonic::builtins::functor::int_{}(pythonic::numpy::functor::floor{}(pythonic::operator_::div(pythonic::operator_::sub(pythonic::operator_::mul(ng, i), h), mg))), 1L), 0L), n_);
        maxj = pythonic::builtins::functor::min{}(pythonic::builtins::functor::int_{}(pythonic::numpy::functor::ceil{}(pythonic::operator_::div(pythonic::operator_::add(pythonic::operator_::mul(ng, i), h), mg))), pythonic::operator_::add(n_, 1L));
        {
          __type161 val;
          if (pythonic::operator_::le(maxj, minj))
          {
            return 1.0;
          }
          else
          {
            val = (((bool)pythonic::operator_::eq(minj, 0L)) ? typename __combined<decltype(0.0), decltype(1.0)>::type(0.0) : typename __combined<decltype(0.0), decltype(1.0)>::type(1.0));
            {
              long  __target139832507554640 = pythonic::operator_::sub(maxj, minj);
              for (long  jj=0L; jj < __target139832507554640; jj += 1L)
              {
                typename pythonic::assignable_noescape<decltype(pythonic::operator_::add(jj, minj))>::type j = pythonic::operator_::add(jj, minj);
                val = pythonic::operator_::div(pythonic::operator_::add(pythonic::operator_::mul(A[pythonic::operator_::sub(pythonic::operator_::add(jj, minj), lastminj)], i), pythonic::operator_::mul(val, j)), pythonic::operator_::add(i, j));
                A[jj] = val;
              }
            }
            curlen = pythonic::operator_::sub(maxj, minj);
            if (pythonic::operator_::gt(std::get<1>(__tuple2), curlen))
            {
              A[pythonic::types::contiguous_slice(pythonic::operator_::sub(maxj, minj),pythonic::operator_::add(pythonic::operator_::sub(maxj, minj), pythonic::operator_::sub(std::get<1>(__tuple2), curlen)))] = 1L;
            }
          }
        }
      }
    }
    return A[pythonic::operator_::sub(pythonic::operator_::sub(maxj, minj), 1L)];
  }
  template <typename argument_type0 >
  inline
  typename _a_ij_Aij_Dij2::type<argument_type0>::result_type _a_ij_Aij_Dij2::operator()(argument_type0&& A) const
  {
    typedef long __type0;
    typedef typename pythonic::assignable<__type0>::type __type1;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type2;
    typedef __type2 __type3;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type4;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type3>())) __type6;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type6>::type>::type __type7;
    typedef typename pythonic::lazy<__type7>::type __type8;
    typedef __type8 __type9;
    typedef decltype(std::declval<__type4>()(std::declval<__type9>())) __type10;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type10>::type::iterator>::value_type>::type __type11;
    typedef __type11 __type12;
    typedef typename std::tuple_element<1,typename std::remove_reference<__type6>::type>::type __type13;
    typedef typename pythonic::lazy<__type13>::type __type14;
    typedef __type14 __type15;
    typedef decltype(std::declval<__type4>()(std::declval<__type15>())) __type16;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type16>::type::iterator>::value_type>::type __type17;
    typedef __type17 __type18;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type12>(), std::declval<__type18>())) __type19;
    typedef decltype(std::declval<__type3>()[std::declval<__type19>()]) __type20;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::square{})>::type>::type __type21;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::sum{})>::type>::type __type22;
    typedef typename pythonic::assignable<__type3>::type __type24;
    typedef typename __combined<__type24,__type3>::type __type26;
    typedef __type26 __type27;
    typedef pythonic::types::contiguous_slice __type28;
    typedef decltype(std::declval<__type27>()(std::declval<__type28>(), std::declval<__type28>())) __type29;
    typedef decltype(std::declval<__type22>()(std::declval<__type29>())) __type30;
    typedef decltype(pythonic::operator_::add(std::declval<__type30>(), std::declval<__type30>())) __type33;
    typedef typename __combined<__type3,__type3>::type __type34;
    typedef typename pythonic::assignable<__type34>::type __type35;
    typedef __type35 __type36;
    typedef decltype(std::declval<__type36>()(std::declval<__type28>(), std::declval<__type28>())) __type37;
    typedef decltype(std::declval<__type22>()(std::declval<__type37>())) __type38;
    typedef decltype(pythonic::operator_::add(std::declval<__type38>(), std::declval<__type38>())) __type41;
    typedef decltype(pythonic::operator_::sub(std::declval<__type33>(), std::declval<__type41>())) __type42;
    typedef decltype(std::declval<__type21>()(std::declval<__type42>())) __type43;
    typedef decltype(pythonic::operator_::mul(std::declval<__type20>(), std::declval<__type43>())) __type44;
    typedef decltype(pythonic::operator_::add(std::declval<__type1>(), std::declval<__type44>())) __type45;
    typedef typename __combined<__type1,__type45>::type __type46;
    typedef typename __combined<__type46,__type44>::type __type47;
    typedef typename pythonic::assignable<__type47>::type __type48;
    typedef typename pythonic::assignable<__type26>::type __type49;
    typedef typename pythonic::assignable<__type35>::type __type50;
    typename pythonic::lazy<decltype(std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, A)))>::type m = std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, A));
    typename pythonic::lazy<decltype(std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, A)))>::type n = std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, A));
    __type48 count = 0L;
    {
      long  __target139832508003904 = m;
      for (long  i=0L; i < __target139832508003904; i += 1L)
      {
        {
          long  __target139832508005632 = n;
          for (long  j=0L; j < __target139832508005632; j += 1L)
          {
            __type49 __pythran_inline_AijA2 = A;
            typename pythonic::assignable_noescape<decltype(i)>::type __pythran_inline_Aiji2 = i;
            typename pythonic::assignable_noescape<decltype(j)>::type __pythran_inline_Aijj2 = j;
            __type50 __pythran_inline_DijA3 = A;
            typename pythonic::assignable_noescape<decltype(i)>::type __pythran_inline_Diji3 = i;
            typename pythonic::assignable_noescape<decltype(j)>::type __pythran_inline_Dijj3 = j;
            count += pythonic::operator_::mul(A.fast(pythonic::types::make_tuple(i, j)), pythonic::numpy::functor::square{}(pythonic::operator_::sub(pythonic::operator_::add(pythonic::numpy::functor::sum{}(__pythran_inline_AijA2(pythonic::types::contiguous_slice(pythonic::builtins::None,__pythran_inline_Aiji2),pythonic::types::contiguous_slice(pythonic::builtins::None,__pythran_inline_Aijj2))), pythonic::numpy::functor::sum{}(__pythran_inline_AijA2(pythonic::types::contiguous_slice(pythonic::operator_::add(__pythran_inline_Aiji2, 1L),pythonic::builtins::None),pythonic::types::contiguous_slice(pythonic::operator_::add(__pythran_inline_Aijj2, 1L),pythonic::builtins::None)))), pythonic::operator_::add(pythonic::numpy::functor::sum{}(__pythran_inline_DijA3(pythonic::types::contiguous_slice(pythonic::operator_::add(__pythran_inline_Diji3, 1L),pythonic::builtins::None),pythonic::types::contiguous_slice(pythonic::builtins::None,__pythran_inline_Dijj3))), pythonic::numpy::functor::sum{}(__pythran_inline_DijA3(pythonic::types::contiguous_slice(pythonic::builtins::None,__pythran_inline_Diji3),pythonic::types::contiguous_slice(pythonic::operator_::add(__pythran_inline_Dijj3, 1L),pythonic::builtins::None)))))));
          }
        }
      }
    }
    return count;
  }
  template <typename argument_type0 >
  inline
  typename _discordant_pairs::type<argument_type0>::result_type _discordant_pairs::operator()(argument_type0&& A) const
  {
    typedef long __type0;
    typedef typename pythonic::assignable<__type0>::type __type1;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type2;
    typedef __type2 __type3;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type4;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type3>())) __type6;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type6>::type>::type __type7;
    typedef typename pythonic::lazy<__type7>::type __type8;
    typedef __type8 __type9;
    typedef decltype(std::declval<__type4>()(std::declval<__type9>())) __type10;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type10>::type::iterator>::value_type>::type __type11;
    typedef __type11 __type12;
    typedef typename std::tuple_element<1,typename std::remove_reference<__type6>::type>::type __type13;
    typedef typename pythonic::lazy<__type13>::type __type14;
    typedef __type14 __type15;
    typedef decltype(std::declval<__type4>()(std::declval<__type15>())) __type16;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type16>::type::iterator>::value_type>::type __type17;
    typedef __type17 __type18;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type12>(), std::declval<__type18>())) __type19;
    typedef decltype(std::declval<__type3>()[std::declval<__type19>()]) __type20;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::sum{})>::type>::type __type21;
    typedef typename pythonic::assignable<__type3>::type __type23;
    typedef __type23 __type24;
    typedef pythonic::types::contiguous_slice __type25;
    typedef decltype(std::declval<__type24>()(std::declval<__type25>(), std::declval<__type25>())) __type26;
    typedef decltype(std::declval<__type21>()(std::declval<__type26>())) __type27;
    typedef decltype(pythonic::operator_::add(std::declval<__type27>(), std::declval<__type27>())) __type30;
    typedef decltype(pythonic::operator_::mul(std::declval<__type20>(), std::declval<__type30>())) __type31;
    typedef decltype(pythonic::operator_::add(std::declval<__type1>(), std::declval<__type31>())) __type32;
    typedef typename __combined<__type1,__type32>::type __type33;
    typedef typename __combined<__type33,__type31>::type __type34;
    typedef typename pythonic::assignable<__type34>::type __type35;
    typename pythonic::lazy<decltype(std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, A)))>::type m = std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, A));
    typename pythonic::lazy<decltype(std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, A)))>::type n = std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, A));
    __type35 count = 0L;
    {
      long  __target139832507980192 = m;
      for (long  i=0L; i < __target139832507980192; i += 1L)
      {
        {
          long  __target139832508002464 = n;
          for (long  j=0L; j < __target139832508002464; j += 1L)
          {
            typename pythonic::assignable_noescape<decltype(A)>::type __pythran_inline_DijA1 = A;
            typename pythonic::assignable_noescape<decltype(i)>::type __pythran_inline_Diji1 = i;
            typename pythonic::assignable_noescape<decltype(j)>::type __pythran_inline_Dijj1 = j;
            count += pythonic::operator_::mul(A.fast(pythonic::types::make_tuple(i, j)), pythonic::operator_::add(pythonic::numpy::functor::sum{}(__pythran_inline_DijA1(pythonic::types::contiguous_slice(pythonic::operator_::add(__pythran_inline_Diji1, 1L),pythonic::builtins::None),pythonic::types::contiguous_slice(pythonic::builtins::None,__pythran_inline_Dijj1))), pythonic::numpy::functor::sum{}(__pythran_inline_DijA1(pythonic::types::contiguous_slice(pythonic::builtins::None,__pythran_inline_Diji1),pythonic::types::contiguous_slice(pythonic::operator_::add(__pythran_inline_Dijj1, 1L),pythonic::builtins::None)))));
          }
        }
      }
    }
    return count;
  }
  template <typename argument_type0 >
  inline
  typename _concordant_pairs::type<argument_type0>::result_type _concordant_pairs::operator()(argument_type0&& A) const
  {
    typedef long __type0;
    typedef typename pythonic::assignable<__type0>::type __type1;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type2;
    typedef __type2 __type3;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type4;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type3>())) __type6;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type6>::type>::type __type7;
    typedef typename pythonic::lazy<__type7>::type __type8;
    typedef __type8 __type9;
    typedef decltype(std::declval<__type4>()(std::declval<__type9>())) __type10;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type10>::type::iterator>::value_type>::type __type11;
    typedef __type11 __type12;
    typedef typename std::tuple_element<1,typename std::remove_reference<__type6>::type>::type __type13;
    typedef typename pythonic::lazy<__type13>::type __type14;
    typedef __type14 __type15;
    typedef decltype(std::declval<__type4>()(std::declval<__type15>())) __type16;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type16>::type::iterator>::value_type>::type __type17;
    typedef __type17 __type18;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type12>(), std::declval<__type18>())) __type19;
    typedef decltype(std::declval<__type3>()[std::declval<__type19>()]) __type20;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::sum{})>::type>::type __type21;
    typedef typename pythonic::assignable<__type3>::type __type23;
    typedef __type23 __type24;
    typedef pythonic::types::contiguous_slice __type25;
    typedef decltype(std::declval<__type24>()(std::declval<__type25>(), std::declval<__type25>())) __type26;
    typedef decltype(std::declval<__type21>()(std::declval<__type26>())) __type27;
    typedef decltype(pythonic::operator_::add(std::declval<__type27>(), std::declval<__type27>())) __type30;
    typedef decltype(pythonic::operator_::mul(std::declval<__type20>(), std::declval<__type30>())) __type31;
    typedef decltype(pythonic::operator_::add(std::declval<__type1>(), std::declval<__type31>())) __type32;
    typedef typename __combined<__type1,__type32>::type __type33;
    typedef typename __combined<__type33,__type31>::type __type34;
    typedef typename pythonic::assignable<__type34>::type __type35;
    typename pythonic::lazy<decltype(std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, A)))>::type m = std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, A));
    typename pythonic::lazy<decltype(std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, A)))>::type n = std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, A));
    __type35 count = 0L;
    {
      long  __target139832507700416 = m;
      for (long  i=0L; i < __target139832507700416; i += 1L)
      {
        {
          long  __target139832507978752 = n;
          for (long  j=0L; j < __target139832507978752; j += 1L)
          {
            typename pythonic::assignable_noescape<decltype(A)>::type __pythran_inline_AijA0 = A;
            typename pythonic::assignable_noescape<decltype(i)>::type __pythran_inline_Aiji0 = i;
            typename pythonic::assignable_noescape<decltype(j)>::type __pythran_inline_Aijj0 = j;
            count += pythonic::operator_::mul(A.fast(pythonic::types::make_tuple(i, j)), pythonic::operator_::add(pythonic::numpy::functor::sum{}(__pythran_inline_AijA0(pythonic::types::contiguous_slice(pythonic::builtins::None,__pythran_inline_Aiji0),pythonic::types::contiguous_slice(pythonic::builtins::None,__pythran_inline_Aijj0))), pythonic::numpy::functor::sum{}(__pythran_inline_AijA0(pythonic::types::contiguous_slice(pythonic::operator_::add(__pythran_inline_Aiji0, 1L),pythonic::builtins::None),pythonic::types::contiguous_slice(pythonic::operator_::add(__pythran_inline_Aijj0, 1L),pythonic::builtins::None)))));
          }
        }
      }
    }
    return count;
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
  inline
  typename _Dij::type<argument_type0, argument_type1, argument_type2>::result_type _Dij::operator()(argument_type0&& A, argument_type1&& i, argument_type2&& j) const
  {
    return pythonic::operator_::add(pythonic::numpy::functor::sum{}(A(pythonic::types::contiguous_slice(pythonic::operator_::add(i, 1L),pythonic::builtins::None),pythonic::types::contiguous_slice(pythonic::builtins::None,j))), pythonic::numpy::functor::sum{}(A(pythonic::types::contiguous_slice(pythonic::builtins::None,i),pythonic::types::contiguous_slice(pythonic::operator_::add(j, 1L),pythonic::builtins::None))));
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
  inline
  typename _Aij::type<argument_type0, argument_type1, argument_type2>::result_type _Aij::operator()(argument_type0&& A, argument_type1&& i, argument_type2&& j) const
  {
    return pythonic::operator_::add(pythonic::numpy::functor::sum{}(A(pythonic::types::contiguous_slice(pythonic::builtins::None,i),pythonic::types::contiguous_slice(pythonic::builtins::None,j))), pythonic::numpy::functor::sum{}(A(pythonic::types::contiguous_slice(pythonic::operator_::add(i, 1L),pythonic::builtins::None),pythonic::types::contiguous_slice(pythonic::operator_::add(j, 1L),pythonic::builtins::None))));
  }
}
#include <pythonic/python/exception_handler.hpp>
#ifdef ENABLE_PYTHON_MODULE
inline
typename __pythran__hypotests_pythran::_compute_outer_prob_inside_method::type<npy_int64, npy_int64, npy_int64, npy_int64>::result_type _compute_outer_prob_inside_method0(npy_int64&& m, npy_int64&& n, npy_int64&& g, npy_int64&& h) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_compute_outer_prob_inside_method()(m, n, g, h);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__hypotests_pythran::_a_ij_Aij_Dij2::type<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>::result_type _a_ij_Aij_Dij20(pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>&& A) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_a_ij_Aij_Dij2()(A);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__hypotests_pythran::_a_ij_Aij_Dij2::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>::result_type _a_ij_Aij_Dij21(pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>&& A) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_a_ij_Aij_Dij2()(A);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__hypotests_pythran::_a_ij_Aij_Dij2::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>::result_type _a_ij_Aij_Dij22(pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& A) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_a_ij_Aij_Dij2()(A);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__hypotests_pythran::_a_ij_Aij_Dij2::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>::result_type _a_ij_Aij_Dij23(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& A) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_a_ij_Aij_Dij2()(A);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__hypotests_pythran::_discordant_pairs::type<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>::result_type _discordant_pairs0(pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>&& A) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_discordant_pairs()(A);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__hypotests_pythran::_discordant_pairs::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>::result_type _discordant_pairs1(pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>&& A) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_discordant_pairs()(A);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__hypotests_pythran::_discordant_pairs::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>::result_type _discordant_pairs2(pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& A) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_discordant_pairs()(A);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__hypotests_pythran::_discordant_pairs::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>::result_type _discordant_pairs3(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& A) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_discordant_pairs()(A);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__hypotests_pythran::_concordant_pairs::type<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>::result_type _concordant_pairs0(pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>&& A) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_concordant_pairs()(A);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__hypotests_pythran::_concordant_pairs::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>::result_type _concordant_pairs1(pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>&& A) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_concordant_pairs()(A);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__hypotests_pythran::_concordant_pairs::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>::result_type _concordant_pairs2(pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& A) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_concordant_pairs()(A);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__hypotests_pythran::_concordant_pairs::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>::result_type _concordant_pairs3(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& A) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_concordant_pairs()(A);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__hypotests_pythran::_Dij::type<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>, long, long>::result_type _Dij0(pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>&& A, long&& i, long&& j) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_Dij()(A, i, j);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__hypotests_pythran::_Dij::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>, long, long>::result_type _Dij1(pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>&& A, long&& i, long&& j) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_Dij()(A, i, j);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__hypotests_pythran::_Dij::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, long, long>::result_type _Dij2(pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& A, long&& i, long&& j) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_Dij()(A, i, j);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__hypotests_pythran::_Dij::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, long, long>::result_type _Dij3(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& A, long&& i, long&& j) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_Dij()(A, i, j);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__hypotests_pythran::_Aij::type<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>, long, long>::result_type _Aij0(pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>&& A, long&& i, long&& j) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_Aij()(A, i, j);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__hypotests_pythran::_Aij::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>, long, long>::result_type _Aij1(pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>&& A, long&& i, long&& j) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_Aij()(A, i, j);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__hypotests_pythran::_Aij::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, long, long>::result_type _Aij2(pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& A, long&& i, long&& j) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_Aij()(A, i, j);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__hypotests_pythran::_Aij::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, long, long>::result_type _Aij3(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& A, long&& i, long&& j) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_Aij()(A, i, j);
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
__pythran_wrap__compute_outer_prob_inside_method0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    
    char const* keywords[] = {"m", "n", "g", "h",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<npy_int64>(args_obj[0]) && is_convertible<npy_int64>(args_obj[1]) && is_convertible<npy_int64>(args_obj[2]) && is_convertible<npy_int64>(args_obj[3]))
        return to_python(_compute_outer_prob_inside_method0(from_python<npy_int64>(args_obj[0]), from_python<npy_int64>(args_obj[1]), from_python<npy_int64>(args_obj[2]), from_python<npy_int64>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__a_ij_Aij_Dij20(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[1+1];
    
    char const* keywords[] = {"A",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "O",
                                     (char**)keywords , &args_obj[0]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[0]))
        return to_python(_a_ij_Aij_Dij20(from_python<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[0])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__a_ij_Aij_Dij21(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[1+1];
    
    char const* keywords[] = {"A",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "O",
                                     (char**)keywords , &args_obj[0]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[0]))
        return to_python(_a_ij_Aij_Dij21(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[0])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__a_ij_Aij_Dij22(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[1+1];
    
    char const* keywords[] = {"A",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "O",
                                     (char**)keywords , &args_obj[0]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]))
        return to_python(_a_ij_Aij_Dij22(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__a_ij_Aij_Dij23(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[1+1];
    
    char const* keywords[] = {"A",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "O",
                                     (char**)keywords , &args_obj[0]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]))
        return to_python(_a_ij_Aij_Dij23(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__discordant_pairs0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[1+1];
    
    char const* keywords[] = {"A",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "O",
                                     (char**)keywords , &args_obj[0]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[0]))
        return to_python(_discordant_pairs0(from_python<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[0])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__discordant_pairs1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[1+1];
    
    char const* keywords[] = {"A",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "O",
                                     (char**)keywords , &args_obj[0]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[0]))
        return to_python(_discordant_pairs1(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[0])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__discordant_pairs2(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[1+1];
    
    char const* keywords[] = {"A",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "O",
                                     (char**)keywords , &args_obj[0]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]))
        return to_python(_discordant_pairs2(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__discordant_pairs3(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[1+1];
    
    char const* keywords[] = {"A",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "O",
                                     (char**)keywords , &args_obj[0]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]))
        return to_python(_discordant_pairs3(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__concordant_pairs0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[1+1];
    
    char const* keywords[] = {"A",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "O",
                                     (char**)keywords , &args_obj[0]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[0]))
        return to_python(_concordant_pairs0(from_python<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[0])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__concordant_pairs1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[1+1];
    
    char const* keywords[] = {"A",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "O",
                                     (char**)keywords , &args_obj[0]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[0]))
        return to_python(_concordant_pairs1(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[0])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__concordant_pairs2(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[1+1];
    
    char const* keywords[] = {"A",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "O",
                                     (char**)keywords , &args_obj[0]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]))
        return to_python(_concordant_pairs2(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__concordant_pairs3(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[1+1];
    
    char const* keywords[] = {"A",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "O",
                                     (char**)keywords , &args_obj[0]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]))
        return to_python(_concordant_pairs3(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__Dij0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    
    char const* keywords[] = {"A", "i", "j",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(_Dij0(from_python<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<long>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__Dij1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    
    char const* keywords[] = {"A", "i", "j",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(_Dij1(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<long>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__Dij2(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    
    char const* keywords[] = {"A", "i", "j",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(_Dij2(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<long>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__Dij3(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    
    char const* keywords[] = {"A", "i", "j",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(_Dij3(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<long>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__Aij0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    
    char const* keywords[] = {"A", "i", "j",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(_Aij0(from_python<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<long>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__Aij1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    
    char const* keywords[] = {"A", "i", "j",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(_Aij1(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<long>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__Aij2(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    
    char const* keywords[] = {"A", "i", "j",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(_Aij2(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<long>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__Aij3(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    
    char const* keywords[] = {"A", "i", "j",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(_Aij3(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<long>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

            static PyObject *
            __pythran_wrapall__compute_outer_prob_inside_method(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap__compute_outer_prob_inside_method0(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "_compute_outer_prob_inside_method", "\n""    - _compute_outer_prob_inside_method(int64, int64, int64, int64)", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall__a_ij_Aij_Dij2(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap__a_ij_Aij_Dij20(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__a_ij_Aij_Dij21(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__a_ij_Aij_Dij22(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__a_ij_Aij_Dij23(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "_a_ij_Aij_Dij2", "\n""    - _a_ij_Aij_Dij2(int[:,:])\n""    - _a_ij_Aij_Dij2(float[:,:])", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall__discordant_pairs(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap__discordant_pairs0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__discordant_pairs1(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__discordant_pairs2(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__discordant_pairs3(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "_discordant_pairs", "\n""    - _discordant_pairs(int[:,:])\n""    - _discordant_pairs(float[:,:])", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall__concordant_pairs(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap__concordant_pairs0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__concordant_pairs1(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__concordant_pairs2(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__concordant_pairs3(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "_concordant_pairs", "\n""    - _concordant_pairs(int[:,:])\n""    - _concordant_pairs(float[:,:])", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall__Dij(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap__Dij0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__Dij1(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__Dij2(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__Dij3(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "_Dij", "\n""    - _Dij(int[:,:], int, int)\n""    - _Dij(float[:,:], int, int)", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall__Aij(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap__Aij0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__Aij1(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__Aij2(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__Aij3(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "_Aij", "\n""    - _Aij(int[:,:], int, int)\n""    - _Aij(float[:,:], int, int)", args, kw);
                });
            }


static PyMethodDef Methods[] = {
    {
    "_compute_outer_prob_inside_method",
    (PyCFunction)__pythran_wrapall__compute_outer_prob_inside_method,
    METH_VARARGS | METH_KEYWORDS,
    "\n""Count the proportion of paths that do not stay strictly inside two\n""diagonal lines.\n""\n""Supported prototypes:\n""\n""- _compute_outer_prob_inside_method(int64, int64, int64, int64)\n""\n""Parameters\n""----------\n""m : integer\n""    m > 0\n""n : integer\n""    n > 0\n""g : integer\n""    g is greatest common divisor of m and n\n""h : integer\n""    0 <= h <= lcm(m,n)\n""\n""Returns\n""-------\n""p : float\n""    The proportion of paths that do not stay inside the two lines.\n""\n""The classical algorithm counts the integer lattice paths from (0, 0)\n""to (m, n) which satisfy |x/m - y/n| < h / lcm(m, n).\n""The paths make steps of size +1 in either positive x or positive y\n""directions.\n""We are, however, interested in 1 - proportion to computes p-values,\n""so we change the recursion to compute 1 - p directly while staying\n""within the \"inside method\" a described by Hodges.\n""\n""We generally follow Hodges' treatment of Drion/Gnedenko/Korolyuk.\n""Hodges, J.L. Jr.,\n""\"The Significance Probability of the Smirnov Two-Sample Test,\"\n""Arkiv fiur Matematik, 3, No. 43 (1958), 469-86.\n""\n""For the recursion for 1-p see\n""Viehmann, T.: \"Numerically more stable computation of the p-values\n""for the two-sample Kolmogorov-Smirnov test,\" arXiv: 2102.08037\n""\n"""},{
    "_a_ij_Aij_Dij2",
    (PyCFunction)__pythran_wrapall__a_ij_Aij_Dij2,
    METH_VARARGS | METH_KEYWORDS,
    "A term that appears in the ASE of Kendall's tau and Somers' D.\n""\n""    Supported prototypes:\n""\n""    - _a_ij_Aij_Dij2(int[:,:])\n""    - _a_ij_Aij_Dij2(float[:,:])"},{
    "_discordant_pairs",
    (PyCFunction)__pythran_wrapall__discordant_pairs,
    METH_VARARGS | METH_KEYWORDS,
    "Twice the number of discordant pairs, excluding ties.\n""\n""    Supported prototypes:\n""\n""    - _discordant_pairs(int[:,:])\n""    - _discordant_pairs(float[:,:])"},{
    "_concordant_pairs",
    (PyCFunction)__pythran_wrapall__concordant_pairs,
    METH_VARARGS | METH_KEYWORDS,
    "Twice the number of concordant pairs, excluding ties.\n""\n""    Supported prototypes:\n""\n""    - _concordant_pairs(int[:,:])\n""    - _concordant_pairs(float[:,:])"},{
    "_Dij",
    (PyCFunction)__pythran_wrapall__Dij,
    METH_VARARGS | METH_KEYWORDS,
    "Sum of lower-left and upper-right blocks of contingency table.\n""\n""    Supported prototypes:\n""\n""    - _Dij(int[:,:], int, int)\n""    - _Dij(float[:,:], int, int)"},{
    "_Aij",
    (PyCFunction)__pythran_wrapall__Aij,
    METH_VARARGS | METH_KEYWORDS,
    "Sum of upper-left and lower right blocks of contingency table.\n""\n""    Supported prototypes:\n""\n""    - _Aij(int[:,:], int, int)\n""    - _Aij(float[:,:], int, int)"},
    {NULL, NULL, 0, NULL}
};


#if PY_MAJOR_VERSION >= 3
  static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "_hypotests_pythran",            /* m_name */
    "",         /* m_doc */
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
PYTHRAN_MODULE_INIT(_hypotests_pythran)(void)
#ifndef _WIN32
__attribute__ ((visibility("default")))
#if defined(GNUC) && !defined(__clang__)
__attribute__ ((externally_visible))
#endif
#endif
;
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(_hypotests_pythran)(void) {
    import_array()
    #if PY_MAJOR_VERSION >= 3
    PyObject* theModule = PyModule_Create(&moduledef);
    #else
    PyObject* theModule = Py_InitModule3("_hypotests_pythran",
                                         Methods,
                                         ""
    );
    #endif
    if(! theModule)
        PYTHRAN_RETURN;
    PyObject * theDoc = Py_BuildValue("(sss)",
                                      "0.11.0",
                                      "2022-05-16 07:20:01.284781",
                                      "1944b45cd2d96e51f059f1d6e1fa8ce83c696cf7987b37e502235695f6b566c1");
    if(! theDoc)
        PYTHRAN_RETURN;
    PyModule_AddObject(theModule,
                       "__pythran__",
                       theDoc);


    PYTHRAN_RETURN;
}

#endif
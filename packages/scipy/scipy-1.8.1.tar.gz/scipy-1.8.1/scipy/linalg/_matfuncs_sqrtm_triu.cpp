#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/types/tuple.hpp>
#include <pythonic/include/types/list.hpp>
#include <pythonic/include/types/int.hpp>
#include <pythonic/include/types/float64.hpp>
#include <pythonic/include/types/complex128.hpp>
#include <pythonic/include/types/ndarray.hpp>
#include <pythonic/include/types/int64.hpp>
#include <pythonic/include/types/numpy_texpr.hpp>
#include <pythonic/types/ndarray.hpp>
#include <pythonic/types/numpy_texpr.hpp>
#include <pythonic/types/tuple.hpp>
#include <pythonic/types/float64.hpp>
#include <pythonic/types/complex128.hpp>
#include <pythonic/types/int64.hpp>
#include <pythonic/types/int.hpp>
#include <pythonic/types/list.hpp>
#include <pythonic/include/builtins/None.hpp>
#include <pythonic/include/builtins/RuntimeError.hpp>
#include <pythonic/include/builtins/pythran/and_.hpp>
#include <pythonic/include/builtins/range.hpp>
#include <pythonic/include/builtins/tuple.hpp>
#include <pythonic/include/operator_/add.hpp>
#include <pythonic/include/operator_/div.hpp>
#include <pythonic/include/operator_/eq.hpp>
#include <pythonic/include/operator_/gt.hpp>
#include <pythonic/include/operator_/iadd.hpp>
#include <pythonic/include/operator_/mul.hpp>
#include <pythonic/include/operator_/ne.hpp>
#include <pythonic/include/operator_/sub.hpp>
#include <pythonic/include/types/str.hpp>
#include <pythonic/builtins/None.hpp>
#include <pythonic/builtins/RuntimeError.hpp>
#include <pythonic/builtins/pythran/and_.hpp>
#include <pythonic/builtins/range.hpp>
#include <pythonic/builtins/tuple.hpp>
#include <pythonic/operator_/add.hpp>
#include <pythonic/operator_/div.hpp>
#include <pythonic/operator_/eq.hpp>
#include <pythonic/operator_/gt.hpp>
#include <pythonic/operator_/iadd.hpp>
#include <pythonic/operator_/mul.hpp>
#include <pythonic/operator_/ne.hpp>
#include <pythonic/operator_/sub.hpp>
#include <pythonic/types/str.hpp>
namespace __pythran__matfuncs_sqrtm_triu
{
  struct within_block_loop
  {
    typedef void callable;
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type0;
      typedef __type0 __type1;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type2;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type3;
      typedef __type3 __type4;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type4>::type::iterator>::value_type>::type __type5;
      typedef std::integral_constant<long,1> __type6;
      typedef __type5 __type7;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type7>::type>::type __type8;
      typedef indexable_container<__type6, typename std::remove_reference<__type8>::type> __type9;
      typedef typename __combined<__type5,__type9>::type __type10;
      typedef __type10 __type11;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type11>::type>::type __type12;
      typedef typename pythonic::lazy<__type12>::type __type13;
      typedef __type13 __type14;
      typedef typename pythonic::lazy<__type8>::type __type15;
      typedef __type15 __type16;
      typedef decltype(std::declval<__type2>()(std::declval<__type14>(), std::declval<__type16>())) __type17;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type17>::type::iterator>::value_type>::type __type18;
      typedef __type18 __type19;
      typedef long __type20;
      typedef decltype(pythonic::operator_::sub(std::declval<__type19>(), std::declval<__type20>())) __type21;
      typedef decltype(pythonic::operator_::sub(std::declval<__type14>(), std::declval<__type20>())) __type23;
      typedef decltype(std::declval<__type2>()(std::declval<__type21>(), std::declval<__type23>(), std::declval<__type20>())) __type24;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type24>::type::iterator>::value_type>::type __type25;
      typedef __type25 __type26;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type26>(), std::declval<__type19>())) __type28;
      typedef decltype(std::declval<__type1>()[std::declval<__type28>()]) __type29;
      typedef typename pythonic::assignable<__type20>::type __type30;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type31;
      typedef __type31 __type32;
      typedef decltype(pythonic::operator_::add(std::declval<__type26>(), std::declval<__type20>())) __type35;
      typedef decltype(std::declval<__type2>()(std::declval<__type35>(), std::declval<__type19>())) __type37;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type37>::type::iterator>::value_type>::type __type38;
      typedef __type38 __type39;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type26>(), std::declval<__type39>())) __type40;
      typedef decltype(std::declval<__type32>()[std::declval<__type40>()]) __type41;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type39>(), std::declval<__type19>())) __type45;
      typedef decltype(std::declval<__type32>()[std::declval<__type45>()]) __type46;
      typedef decltype(pythonic::operator_::mul(std::declval<__type41>(), std::declval<__type46>())) __type47;
      typedef decltype(pythonic::operator_::add(std::declval<__type30>(), std::declval<__type47>())) __type48;
      typedef typename __combined<__type30,__type48>::type __type49;
      typedef typename __combined<__type49,__type47>::type __type50;
      typedef __type50 __type51;
      typedef decltype(pythonic::operator_::sub(std::declval<__type29>(), std::declval<__type51>())) __type52;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type26>(), std::declval<__type26>())) __type56;
      typedef decltype(std::declval<__type32>()[std::declval<__type56>()]) __type57;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type19>(), std::declval<__type19>())) __type61;
      typedef decltype(std::declval<__type32>()[std::declval<__type61>()]) __type62;
      typedef decltype(pythonic::operator_::add(std::declval<__type57>(), std::declval<__type62>())) __type63;
      typedef typename pythonic::assignable<__type63>::type __type64;
      typedef __type64 __type65;
      typedef decltype(pythonic::operator_::div(std::declval<__type52>(), std::declval<__type65>())) __type66;
      typedef __type66 __type67;
      typedef __type28 __type71;
      typedef pythonic::types::none_type __type72;
      typedef typename pythonic::returnable<__type72>::type __type73;
      typedef __type67 __ptype0;
      typedef __type71 __ptype1;
      typedef __type73 result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
    inline
    typename type<argument_type0, argument_type1, argument_type2, argument_type3>::result_type operator()(argument_type0&& R, argument_type1&& T, argument_type2&& start_stop_pairs, argument_type3&& nblocks) const
    ;
  }  ;
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
  inline
  typename within_block_loop::type<argument_type0, argument_type1, argument_type2, argument_type3>::result_type within_block_loop::operator()(argument_type0&& R, argument_type1&& T, argument_type2&& start_stop_pairs, argument_type3&& nblocks) const
  {
    typedef long __type0;
    typedef typename pythonic::assignable<__type0>::type __type1;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type2;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type3;
    typedef __type3 __type4;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type5;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type6;
    typedef __type6 __type7;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type7>::type::iterator>::value_type>::type __type8;
    typedef std::integral_constant<long,1> __type9;
    typedef __type8 __type10;
    typedef typename std::tuple_element<1,typename std::remove_reference<__type10>::type>::type __type11;
    typedef indexable_container<__type9, typename std::remove_reference<__type11>::type> __type12;
    typedef std::integral_constant<long,0> __type13;
    typedef typename __combined<__type8,__type12>::type __type14;
    typedef __type14 __type15;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type15>::type>::type __type16;
    typedef indexable_container<__type13, typename std::remove_reference<__type16>::type> __type17;
    typedef typename __combined<__type8,__type12,__type17>::type __type18;
    typedef typename pythonic::lazy<__type16>::type __type19;
    typedef __type19 __type20;
    typedef typename pythonic::lazy<__type11>::type __type21;
    typedef __type21 __type22;
    typedef decltype(std::declval<__type5>()(std::declval<__type20>(), std::declval<__type22>())) __type23;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type23>::type::iterator>::value_type>::type __type24;
    typedef __type24 __type25;
    typedef decltype(pythonic::operator_::sub(std::declval<__type25>(), std::declval<__type0>())) __type26;
    typedef decltype(pythonic::operator_::sub(std::declval<__type20>(), std::declval<__type0>())) __type28;
    typedef decltype(std::declval<__type5>()(std::declval<__type26>(), std::declval<__type28>(), std::declval<__type0>())) __type29;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type29>::type::iterator>::value_type>::type __type30;
    typedef __type30 __type31;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type31>(), std::declval<__type25>())) __type33;
    typedef decltype(std::declval<__type4>()[std::declval<__type33>()]) __type34;
    typedef __type2 __type35;
    typedef decltype(pythonic::operator_::add(std::declval<__type31>(), std::declval<__type0>())) __type38;
    typedef decltype(std::declval<__type5>()(std::declval<__type38>(), std::declval<__type25>())) __type40;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type40>::type::iterator>::value_type>::type __type41;
    typedef __type41 __type42;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type31>(), std::declval<__type42>())) __type43;
    typedef decltype(std::declval<__type35>()[std::declval<__type43>()]) __type44;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type42>(), std::declval<__type25>())) __type48;
    typedef decltype(std::declval<__type35>()[std::declval<__type48>()]) __type49;
    typedef decltype(pythonic::operator_::mul(std::declval<__type44>(), std::declval<__type49>())) __type50;
    typedef decltype(pythonic::operator_::add(std::declval<__type1>(), std::declval<__type50>())) __type51;
    typedef typename __combined<__type1,__type51>::type __type52;
    typedef typename __combined<__type52,__type50>::type __type53;
    typedef __type53 __type54;
    typedef decltype(pythonic::operator_::sub(std::declval<__type34>(), std::declval<__type54>())) __type55;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type31>(), std::declval<__type31>())) __type59;
    typedef decltype(std::declval<__type35>()[std::declval<__type59>()]) __type60;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type25>(), std::declval<__type25>())) __type64;
    typedef decltype(std::declval<__type35>()[std::declval<__type64>()]) __type65;
    typedef decltype(pythonic::operator_::add(std::declval<__type60>(), std::declval<__type65>())) __type66;
    typedef typename pythonic::assignable<__type66>::type __type67;
    typedef __type67 __type68;
    typedef decltype(pythonic::operator_::div(std::declval<__type55>(), std::declval<__type68>())) __type69;
    typedef container<typename std::remove_reference<__type69>::type> __type70;
    typedef indexable<__type33> __type74;
    typedef container<typename std::remove_reference<__type0>::type> __type75;
    typedef typename __combined<__type2,__type70,__type74,__type75,__type74>::type __type80;
    typedef typename pythonic::assignable<__type53>::type __type81;
    {
      for (auto&& __tuple0: start_stop_pairs)
      {
        typename pythonic::lazy<decltype(std::get<1>(__tuple0))>::type stop = std::get<1>(__tuple0);
        typename pythonic::lazy<decltype(std::get<0>(__tuple0))>::type start = std::get<0>(__tuple0);
        {
          long  __target139832508289712 = stop;
          for (long  j=start; j < __target139832508289712; j += 1L)
          {
            {
              long  __target139832508289232 = pythonic::operator_::sub(start, 1L);
              for (long  i=pythonic::operator_::sub(j, 1L); i > __target139832508289232; i += -1L)
              {
                __type81 s = 0L;
                if (pythonic::operator_::gt(pythonic::operator_::sub(j, i), 1L))
                {
                  {
                    long  __target139832508573200 = j;
                    for (long  k=pythonic::operator_::add(i, 1L); k < __target139832508573200; k += 1L)
                    {
                      s += pythonic::operator_::mul(R[pythonic::types::make_tuple(i, k)], R[pythonic::types::make_tuple(k, j)]);
                    }
                  }
                }
                typename pythonic::assignable_noescape<decltype(pythonic::operator_::add(R[pythonic::types::make_tuple(i, i)], R[pythonic::types::make_tuple(j, j)]))>::type denom = pythonic::operator_::add(R[pythonic::types::make_tuple(i, i)], R[pythonic::types::make_tuple(j, j)]);
                if (pythonic::operator_::ne(denom, 0L))
                {
                  R[pythonic::types::make_tuple(i, j)] = pythonic::operator_::div(pythonic::operator_::sub(T[pythonic::types::make_tuple(i, j)], s), denom);
                }
                else
                {
                  if (pythonic::builtins::pythran::and_([&] () { return pythonic::operator_::eq(denom, 0L); }, [&] () { return pythonic::operator_::eq(pythonic::operator_::sub(T[pythonic::types::make_tuple(i, j)], s), 0L); }))
                  {
                    R[pythonic::types::make_tuple(i, j)] = 0L;
                  }
                  else
                  {
                    throw pythonic::builtins::functor::RuntimeError{}(pythonic::types::str("failed to find the matrix square root"));
                  }
                }
              }
            }
          }
        }
      }
    }
    return pythonic::builtins::None;
  }
}
#include <pythonic/python/exception_handler.hpp>
#ifdef ENABLE_PYTHON_MODULE
inline
typename __pythran__matfuncs_sqrtm_triu::within_block_loop::type<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>, pythonic::types::list<decltype(pythonic::types::make_tuple(std::declval<long>(), std::declval<long>()))>, npy_int64>::result_type within_block_loop0(pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>&& R, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>&& T, pythonic::types::list<decltype(pythonic::types::make_tuple(std::declval<long>(), std::declval<long>()))>&& start_stop_pairs, npy_int64&& nblocks) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__matfuncs_sqrtm_triu::within_block_loop()(R, T, start_stop_pairs, nblocks);
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
typename __pythran__matfuncs_sqrtm_triu::within_block_loop::type<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>, pythonic::types::list<decltype(pythonic::types::make_tuple(std::declval<long>(), std::declval<long>()))>, npy_int64>::result_type within_block_loop1(pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>&& R, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>&& T, pythonic::types::list<decltype(pythonic::types::make_tuple(std::declval<long>(), std::declval<long>()))>&& start_stop_pairs, npy_int64&& nblocks) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__matfuncs_sqrtm_triu::within_block_loop()(R, T, start_stop_pairs, nblocks);
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
typename __pythran__matfuncs_sqrtm_triu::within_block_loop::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>, pythonic::types::list<decltype(pythonic::types::make_tuple(std::declval<long>(), std::declval<long>()))>, npy_int64>::result_type within_block_loop2(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>&& R, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>&& T, pythonic::types::list<decltype(pythonic::types::make_tuple(std::declval<long>(), std::declval<long>()))>&& start_stop_pairs, npy_int64&& nblocks) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__matfuncs_sqrtm_triu::within_block_loop()(R, T, start_stop_pairs, nblocks);
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
typename __pythran__matfuncs_sqrtm_triu::within_block_loop::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>, pythonic::types::list<decltype(pythonic::types::make_tuple(std::declval<long>(), std::declval<long>()))>, npy_int64>::result_type within_block_loop3(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>&& R, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>&& T, pythonic::types::list<decltype(pythonic::types::make_tuple(std::declval<long>(), std::declval<long>()))>&& start_stop_pairs, npy_int64&& nblocks) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__matfuncs_sqrtm_triu::within_block_loop()(R, T, start_stop_pairs, nblocks);
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
typename __pythran__matfuncs_sqrtm_triu::within_block_loop::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, pythonic::types::list<decltype(pythonic::types::make_tuple(std::declval<long>(), std::declval<long>()))>, npy_int64>::result_type within_block_loop4(pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& R, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& T, pythonic::types::list<decltype(pythonic::types::make_tuple(std::declval<long>(), std::declval<long>()))>&& start_stop_pairs, npy_int64&& nblocks) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__matfuncs_sqrtm_triu::within_block_loop()(R, T, start_stop_pairs, nblocks);
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
typename __pythran__matfuncs_sqrtm_triu::within_block_loop::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, pythonic::types::list<decltype(pythonic::types::make_tuple(std::declval<long>(), std::declval<long>()))>, npy_int64>::result_type within_block_loop5(pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& R, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& T, pythonic::types::list<decltype(pythonic::types::make_tuple(std::declval<long>(), std::declval<long>()))>&& start_stop_pairs, npy_int64&& nblocks) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__matfuncs_sqrtm_triu::within_block_loop()(R, T, start_stop_pairs, nblocks);
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
typename __pythran__matfuncs_sqrtm_triu::within_block_loop::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, pythonic::types::list<decltype(pythonic::types::make_tuple(std::declval<long>(), std::declval<long>()))>, npy_int64>::result_type within_block_loop6(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& R, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& T, pythonic::types::list<decltype(pythonic::types::make_tuple(std::declval<long>(), std::declval<long>()))>&& start_stop_pairs, npy_int64&& nblocks) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__matfuncs_sqrtm_triu::within_block_loop()(R, T, start_stop_pairs, nblocks);
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
typename __pythran__matfuncs_sqrtm_triu::within_block_loop::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, pythonic::types::list<decltype(pythonic::types::make_tuple(std::declval<long>(), std::declval<long>()))>, npy_int64>::result_type within_block_loop7(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& R, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& T, pythonic::types::list<decltype(pythonic::types::make_tuple(std::declval<long>(), std::declval<long>()))>&& start_stop_pairs, npy_int64&& nblocks) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__matfuncs_sqrtm_triu::within_block_loop()(R, T, start_stop_pairs, nblocks);
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
__pythran_wrap_within_block_loop0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    
    char const* keywords[] = {"R", "T", "start_stop_pairs", "nblocks",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>(args_obj[1]) && is_convertible<pythonic::types::list<decltype(pythonic::types::make_tuple(std::declval<long>(), std::declval<long>()))>>(args_obj[2]) && is_convertible<npy_int64>(args_obj[3]))
        return to_python(within_block_loop0(from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>(args_obj[1]), from_python<pythonic::types::list<decltype(pythonic::types::make_tuple(std::declval<long>(), std::declval<long>()))>>(args_obj[2]), from_python<npy_int64>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_within_block_loop1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    
    char const* keywords[] = {"R", "T", "start_stop_pairs", "nblocks",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>>(args_obj[1]) && is_convertible<pythonic::types::list<decltype(pythonic::types::make_tuple(std::declval<long>(), std::declval<long>()))>>(args_obj[2]) && is_convertible<npy_int64>(args_obj[3]))
        return to_python(within_block_loop1(from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>>(args_obj[1]), from_python<pythonic::types::list<decltype(pythonic::types::make_tuple(std::declval<long>(), std::declval<long>()))>>(args_obj[2]), from_python<npy_int64>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_within_block_loop2(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    
    char const* keywords[] = {"R", "T", "start_stop_pairs", "nblocks",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>(args_obj[1]) && is_convertible<pythonic::types::list<decltype(pythonic::types::make_tuple(std::declval<long>(), std::declval<long>()))>>(args_obj[2]) && is_convertible<npy_int64>(args_obj[3]))
        return to_python(within_block_loop2(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>(args_obj[1]), from_python<pythonic::types::list<decltype(pythonic::types::make_tuple(std::declval<long>(), std::declval<long>()))>>(args_obj[2]), from_python<npy_int64>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_within_block_loop3(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    
    char const* keywords[] = {"R", "T", "start_stop_pairs", "nblocks",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>>(args_obj[1]) && is_convertible<pythonic::types::list<decltype(pythonic::types::make_tuple(std::declval<long>(), std::declval<long>()))>>(args_obj[2]) && is_convertible<npy_int64>(args_obj[3]))
        return to_python(within_block_loop3(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>>(args_obj[1]), from_python<pythonic::types::list<decltype(pythonic::types::make_tuple(std::declval<long>(), std::declval<long>()))>>(args_obj[2]), from_python<npy_int64>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_within_block_loop4(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    
    char const* keywords[] = {"R", "T", "start_stop_pairs", "nblocks",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[1]) && is_convertible<pythonic::types::list<decltype(pythonic::types::make_tuple(std::declval<long>(), std::declval<long>()))>>(args_obj[2]) && is_convertible<npy_int64>(args_obj[3]))
        return to_python(within_block_loop4(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[1]), from_python<pythonic::types::list<decltype(pythonic::types::make_tuple(std::declval<long>(), std::declval<long>()))>>(args_obj[2]), from_python<npy_int64>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_within_block_loop5(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    
    char const* keywords[] = {"R", "T", "start_stop_pairs", "nblocks",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[1]) && is_convertible<pythonic::types::list<decltype(pythonic::types::make_tuple(std::declval<long>(), std::declval<long>()))>>(args_obj[2]) && is_convertible<npy_int64>(args_obj[3]))
        return to_python(within_block_loop5(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[1]), from_python<pythonic::types::list<decltype(pythonic::types::make_tuple(std::declval<long>(), std::declval<long>()))>>(args_obj[2]), from_python<npy_int64>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_within_block_loop6(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    
    char const* keywords[] = {"R", "T", "start_stop_pairs", "nblocks",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[1]) && is_convertible<pythonic::types::list<decltype(pythonic::types::make_tuple(std::declval<long>(), std::declval<long>()))>>(args_obj[2]) && is_convertible<npy_int64>(args_obj[3]))
        return to_python(within_block_loop6(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[1]), from_python<pythonic::types::list<decltype(pythonic::types::make_tuple(std::declval<long>(), std::declval<long>()))>>(args_obj[2]), from_python<npy_int64>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_within_block_loop7(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    
    char const* keywords[] = {"R", "T", "start_stop_pairs", "nblocks",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[1]) && is_convertible<pythonic::types::list<decltype(pythonic::types::make_tuple(std::declval<long>(), std::declval<long>()))>>(args_obj[2]) && is_convertible<npy_int64>(args_obj[3]))
        return to_python(within_block_loop7(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[1]), from_python<pythonic::types::list<decltype(pythonic::types::make_tuple(std::declval<long>(), std::declval<long>()))>>(args_obj[2]), from_python<npy_int64>(args_obj[3])));
    else {
        return nullptr;
    }
}

            static PyObject *
            __pythran_wrapall_within_block_loop(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_within_block_loop0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_within_block_loop1(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_within_block_loop2(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_within_block_loop3(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_within_block_loop4(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_within_block_loop5(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_within_block_loop6(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_within_block_loop7(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "within_block_loop", "\n""    - within_block_loop(complex128[:,:], complex128[:,:], (int, int) list, int64)\n""    - within_block_loop(float64[:,:], float64[:,:], (int, int) list, int64)", args, kw);
                });
            }


static PyMethodDef Methods[] = {
    {
    "within_block_loop",
    (PyCFunction)__pythran_wrapall_within_block_loop,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n""\n""    - within_block_loop(complex128[:,:], complex128[:,:], (int, int) list, int64)\n""    - within_block_loop(float64[:,:], float64[:,:], (int, int) list, int64)"},
    {NULL, NULL, 0, NULL}
};


#if PY_MAJOR_VERSION >= 3
  static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "_matfuncs_sqrtm_triu",            /* m_name */
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
PYTHRAN_MODULE_INIT(_matfuncs_sqrtm_triu)(void)
#ifndef _WIN32
__attribute__ ((visibility("default")))
#if defined(GNUC) && !defined(__clang__)
__attribute__ ((externally_visible))
#endif
#endif
;
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(_matfuncs_sqrtm_triu)(void) {
    import_array()
    #if PY_MAJOR_VERSION >= 3
    PyObject* theModule = PyModule_Create(&moduledef);
    #else
    PyObject* theModule = Py_InitModule3("_matfuncs_sqrtm_triu",
                                         Methods,
                                         ""
    );
    #endif
    if(! theModule)
        PYTHRAN_RETURN;
    PyObject * theDoc = Py_BuildValue("(sss)",
                                      "0.11.0",
                                      "2022-05-16 07:19:55.345319",
                                      "a0322db4e483f09ff775e69a40dbad00140cb9afebff889e57e3204433ba3ab1");
    if(! theDoc)
        PYTHRAN_RETURN;
    PyModule_AddObject(theModule,
                       "__pythran__",
                       theDoc);


    PYTHRAN_RETURN;
}

#endif